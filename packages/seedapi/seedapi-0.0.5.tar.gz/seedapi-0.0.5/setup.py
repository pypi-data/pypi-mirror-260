import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name="seedapi",
	version="0.0.5",
	author="imrc",
	author_email="imrc@aiit.org.cn",
	description="Api library for Seed Platform",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=["tqdm>=4.60", "requests>=2.22"]
)