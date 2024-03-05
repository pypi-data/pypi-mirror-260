import logging
import os
import json
import time
import urllib.parse
from json import JSONDecodeError

import requests
import mimetypes
from tqdm import tqdm
from typing import List

_logger = logging.getLogger('seedapi')
_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
_logger.addHandler(handler)

#任务模式 长期暴露
TASK_MODEL_LONG_TERM_EXPOSURE = 1

#任务模式 自定义长期暴露
TASK_MODEL_LONG_TERM_EXPOSURE_CUSTOM = 2

#任务模式 短期暴露
TASK_MODEL_SHORT_TERM = 3

#任务模式 自定义短期暴露
TASK_MODEL_SHORT_TERM_CUSTOM = 4

VALID_TASK_MODEL = [TASK_MODEL_LONG_TERM_EXPOSURE, TASK_MODEL_LONG_TERM_EXPOSURE_CUSTOM, TASK_MODEL_SHORT_TERM, TASK_MODEL_SHORT_TERM_CUSTOM]

HOST = 'https://seed.bjmu.edu.cn/api-gate/'


class TaskArgs:
    def to_string(self):
        raise NotImplementedError


class ExtremeWeatherTaskArgs(TaskArgs):

    class AbsoluteInfo:

        def __init__(self, temperature_threshold: List[int], running_days: int):
            self.temperature_threshold = temperature_threshold
            self.running_days = running_days

        def to_dict(self):
            return {
                'temperatureThreshold': self.temperature_threshold,
                'runningDays': self.running_days
            }

    class RelativeInfo:
        def __init__(self, relative_percentile: List[int], running_days: int):
            self.relative_percentile = relative_percentile
            self.running_days = running_days

        def to_dict(self):
            return {
                'relativePercentile': self.relative_percentile,
                'runningDays': self.running_days
            }

    def __init__(self, temperature_threshold: List[int], abs_days: int, relative_percentile: List[int], rel_days: int):
        self.absolute_index = None
        self.relative_index = None

        if temperature_threshold and abs_days > 0:
            self.absolute_index = ExtremeWeatherTaskArgs.AbsoluteInfo(temperature_threshold, abs_days)

        if relative_percentile and rel_days > 0:
            self.relative_index = ExtremeWeatherTaskArgs.RelativeInfo(relative_percentile, rel_days)

        assert self.absolute_index or self.relative_index, 'Extreme Weather Should has at least one args combination'

    def to_string(self):
        output_map = {}
        if self.absolute_index:
            output_map['absoluteIndex'] = self.absolute_index.to_dict()
        if self.relative_index:
            output_map['relativeIndex'] = self.relative_index.to_dict()
        return json.dumps(output_map)


class Task:
    def __init__(self):
        """
        页面上看到的数据产品名称 直接复制 如TAP_PMC
        """
        self.dataset = ''

        """
        任务模式
        """
        self.task_model = 0

        """
        模型匹配任务的特殊参数
        """
        self.task_args = None

        """
        上传的匹配文件，本地文件或文件流
        """
        self.input_file = None

    def with_dataset(self, dataset):
        self.dataset = dataset
        return self

    def with_task_model(self, task_model):
        assert task_model in VALID_TASK_MODEL, 'Task Model error. should in %s'%VALID_TASK_MODEL
        self.task_model = task_model
        return self

    def with_task_args(self, task_args):
        assert isinstance(task_args, TaskArgs), 'Invalid Task Args'
        self.task_args = task_args
        return self

    def with_input_file(self, input_file):
        if isinstance(input_file, str):
            assert os.path.exists(input_file) and os.path.isfile(input_file), 'Input file not exist %s'%input_file
        elif not hasattr(input_file, 'read'):
            raise TypeError('Unsupported file type. Please provide a file path or an opened file object')
        self.input_file = input_file
        return self


    def ready(self):
        return self.dataset and self.task_model and self.input_file



class SeedClient(object):

    CODE_EXPIRED = 100100105
    CODE_UNCOMPLETED = 10110402

    def __init__(self, client_id, secret, timeout=60, wait_download_interval=60, session=requests.Session()):
        self.client_id = client_id
        self.secret = secret
        self.timeout = timeout

        self.wait_download_interval = max(wait_download_interval, 5)

        self.host = HOST
        self.session = session

        self.headers = {'User-Agent': 'SeedClient'}

    def token_expire(self, response):
        try:
            if response.json().get('code') == SeedClient.CODE_EXPIRED:
                _logger.info('Token expire!')
                self.login()
                return True
        except JSONDecodeError:
            return False

    def request_post(self, url, **kwargs):
        params = kwargs.pop('params', None)
        data = kwargs.pop('data', None)
        files = kwargs.pop('files', None)
        request_kwargs = {'headers': self.headers, 'timeout': self.timeout}
        if params:
            request_kwargs['params'] = params
        if data:
            request_kwargs['data'] = data
        if files:
            request_kwargs['files'] = files
        resp = self.session.post(url, **request_kwargs)
        if resp.status_code == 200:
            if self.token_expire(resp):
                return self.request_post(url, **kwargs)
            return resp
        else:
            _logger.error(f'{resp.status_code}, {resp.text}')

    def request_get(self, url):
        resp = self.session.get(url, headers=self.headers, timeout=self.timeout, stream=True)
        if resp.status_code == 200:
            if self.token_expire(resp):
                return self.request_get(url)
            return resp
        else:
            _logger.error(f'{resp.status_code}, {resp.text}')

    def login(self):
        url = self.host + 'auth/auth/token'
        params = {'clientId': self.client_id, 'secret': self.secret}
        resp = self.request_post(url, params=params)
        if resp.status_code != 200 :
            raise Exception('login http error code :%s ', resp.status_code)
        code = resp.json()['code']
        if code != 0:
            raise Exception('login system error code :%s ', code)
        self.headers.update({'AIIT-ZHYL-AUTH': resp.json()['data']['accessToken']})
        return self

    def match(self, task:Task):
        if not task.ready():
            _logger.error('Task info not completed, ignored ')
            return

        url = self.host + 'data/airisk/file/matchedData'
        data = {
            'dataset': task.dataset,
            'taskModel': task.task_model,
            'specialInfo': task.task_args.to_string() if task.task_args else '',
        }

        file = task.input_file
        if isinstance(file, str):
            content_type = mimetypes.guess_type(file)[0]
            with open(file, 'rb') as f:
                files = {
                    'file': (os.path.basename(file), f, content_type)
                }
                resp = self.request_post(url, data=data, files=files)
        else:
            files = {
                'file': file
            }
            resp = self.request_post(url, data=data, files=files)
        if resp.status_code != 200 or resp.json()['code'] != 0:
            _logger.error('upload error')
            return

        download_id = resp.json().get('data')
        return download_id


    def download(self, download_id, target=None):
        if target and os.path.exists(target):
            _logger.warning('Output target file exist, will be replaced %s' % target)

        while True:
            url = f'{self.host}data/airisk/file/downloadByDownloadInfoId?downloadId={download_id}'
            resp = self.request_get(url)
            if resp.status_code != 200:
                _logger.error('download with http error %s', resp.status_code)
                return
            try:
                if resp.json()['code'] == SeedClient.CODE_UNCOMPLETED:
                    _logger.info('task not completed. wait for %s sec', self.wait_download_interval)
                    time.sleep(self.wait_download_interval)
                    continue
                _logger.error('download error with code %s',  resp.json()['code'])
                return
            except JSONDecodeError:
                break

        try:
            total_size = int(resp.headers.get('content-length'))
        except (TypeError, ValueError):
            total_size = None

        content_disposition = resp.headers.get('Content-Disposition')
        file_name_encoded = content_disposition.split('filename*=')[-1]
        file_name = urllib.parse.unquote(file_name_encoded).strip('UTF-8')

        if target is None:
            target = os.path.join('../..', file_name)
        if os.path.isdir(target):
            target = os.path.join(target, file_name)

        filename = os.path.basename(target)
        with tqdm(total=total_size, disable=total_size is None, unit='B', unit_scale=True, desc=f'Downloading - {filename}') as bar:
            with open(target, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
        _logger.info(f'{target} 下载成功！')
