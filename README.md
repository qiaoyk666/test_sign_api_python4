# test-sign-api-python2
### 使用方法

1 安装

```bash
pip install git+https://github.com/qiaoyk666/test-sign-api-python.git
```

2 DataCloudSign使用
```bash
from geovis-cloud-api-node import CertificationSign
import uuid
from datetime import datetime

certificationSign = CertificationSign('your secretId', 'your secretKey')

path = '/v1/cloudapi/certification/industry'
method = 'GET'
body = None
queryString = 'key1=value1&key2&value2'
nonceStr = str(uuid.uuid4())
timestamp = str(round(datetime.now().timestamp() * 1000))
# 获取签名请求头 
headers = certificationSign.sign(path, method, body, queryString, nonceStr, timestamp)
# 请求接口
url = f'https://api1-dev.geovisearth.com/daas/certification-dev{path}'
if (queryString):
    url = f'{url}?{queryString}'
result = certificationSign.request(url, method, headers, body)
```
3 CertificationSign使用
```bash

```
