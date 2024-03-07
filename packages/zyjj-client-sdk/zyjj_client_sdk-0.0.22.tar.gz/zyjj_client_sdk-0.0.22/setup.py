from setuptools import setup, find_packages

setup(
    name='zyjj_client_sdk',
    version='0.0.22',
    description='智游剪辑客户端sdk包',
    url='https://github.com/zyjj-cc/zyjj-client-sdk',
    author='zyjj',
    author_email='zyjj.cc@foxmail.com',
    license='MIT',
    long_description="智游剪辑客户端sdk包",
    packages=find_packages(),
    install_requires=[
        'requests~=2.31.0',
        'paho-mqtt~=1.6.1',
        'ffmpeg-progress-yield~=0.7.8',
        'ffmpeg-python~=0.2.0',
        'cos-python-sdk-v5~=1.9.26',
        'tencentcloud-sdk-python~=3.0.1090'
    ]
)
