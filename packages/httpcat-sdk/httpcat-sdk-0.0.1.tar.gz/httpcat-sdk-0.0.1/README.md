# Httpcat SDK for Python
## Httpcat SDK
Httpcat SDK 配合 httpcat服务项目使用，是httpcat服务的sdk。
使用httpcat sdk方便

## 安装

通过pip安装
```bash
$ pip install httpcat-sdk
```

检查是否安装成功
```bash
(venv) [root@dev ~]# python
Python 3.8.12 (default, Aug  6 2023, 18:06:17)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import httpcat
>>> httpcat.__version__
'0.0.1'
>>>
```

使用:
```
from httpcat.services.storage.uploader import upload_file

# file_path = '/path/to/file'
file_path = '/root/aaa.txt'
upload_token = 'admin_349015:ggjTvfW266vy6KG7zOsqJZCtN3c=:eyJkZWFkbGluZSI6MH0='
upload_url = 'http://httpcat.cn/api/v1/file/upload'

response = upload_file(file_path, upload_token, upload_url)
print(response.text)
```
根据你搭建httpcat，修改upload_token，upload_url信息
upload_token来自httpcat服务上传token管理界面。


正常输出结果：
```bash
>>> print(response.text)
{"errorCode":0,"msg":"success","data":"upload successful!"}
```

