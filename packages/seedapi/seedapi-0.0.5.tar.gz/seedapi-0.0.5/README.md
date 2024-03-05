# SEED平台API使用手册

# 1 安装
```
pip install seedapi
```

# 2 使用
## 1. python环境导入函数seedapi


```python
import seedapi
```

## 2. 匹配暴露数据

调用match函数，设置相应参数，匹配相应暴露数据。

```python
#设置参数
client_id = 'xxxxxx' #API凭证
secret = 'xxxxxxxxxxxxx' #API凭证
dataset = 'ERA5_TEMP_1' #数据产品名称
input_file = r'数据模板.csv' #模板数据地址
task_model = seedapi.TASK_MODEL_LONG_TERM_EXPOSURE #任务模式
output_file = r'result.csv' #暴露数据下载保存地址

# match
client = seedapi.SeedClient(client_id, secret).login()
task = seedapi.Task().with_dataset(dataset).with_task_model(task_model).with_input_file(input_file)
download_id = client.match(task)
```

其中，client\_id和secret为用户的API凭证，获取路径：用户-账号设置-API凭证-重置，复制保存即可。
![image](https://imgur.com/0YypRYk.png)

![image](https://imgur.com/rNH818X.png)

![image](https://imgur.com/U070WAv.png)
dataset、input\_file和task\_model参数依据相应数据产品设置。
以温度数据的长期暴露匹配为例：dataset=‘ERA5\_TEMP\_1’，input\_file=r'长期暴露数据模板.csv'，task\_model=TASK_MODEL_LONG_TERM_EXPOSURE_CUSTOM。
按照平台数据产品相应任务模式下载数据模板，按照模板准备数据。
四种任务模式下task\_model依次为
```
TASK_MODEL_LONG_TERM_EXPOSURE
TASK_MODEL_LONG_TERM_EXPOSURE_CUSTOM
TASK_MODEL_SHORT_TERM
TASK_MODEL_SHORT_TERM_CUSTOM    
```
![image](https://imgur.com/4kQFAaG.png)
## 3. 下载暴露匹配完成数据

等待一段时间后，下载匹配完成的暴露数据，output\_file参数为数据下载保存地址，自行设置，如output\_file = r'result.csv'

```python
# download, wait for a while
client.download(download_id, output_file)
```



> 注意： 如果出现网络连接相关错误请检查本地系统代理，使用国外IP可能导致无法访问平台
