### 使用方法

1 安装

```bash
pip install git+https://github.com/qiaoyk666/test-sign-api-python.git
```

2 DataCloudSign使用
```bash
from geovis_cloud_api_node import CertificationSign
import uuid
from datetime import datetime

certificationSign = CertificationSign('your secretId', 'your secretKey')

path = '/v1/cloudapi/certification/industry'
method = 'GET'
body = None # body为空时，传None
queryString = 'key1=value1&key2&value2' # 无查询参数时，传空字符串
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
from geovis_cloud_api_node import CertificationSign
import uuid
from datetime import datetime

path = '/v1/cloudapi/certification/industry'
method = 'GET'
body = None # body为空时，传None
queryString = '' # 无查询参数时，传空字符串
url = f'https://api1-dev.geovisearth.com/daas/certification-dev{path}'
if (queryString):
    url = f'{url}?{queryString}'
nonceStr = str(uuid.uuid4())
timestamp = str(round(datetime.now().timestamp() * 1000))

certSign = CertificationSign('your secretId', 'your secretKey')
headers = certSign.sign(path, method, body, queryString, nonceStr, timestamp)

result = certSign.request(url, method, headers, body)
```

4 PaymentSign使用
```bash
from geovis_cloud_api_node import PaymentSign
import uuid
from datetime import datetime

path = '/v1/invoice'
method = 'POST'
# body为空时，传None
body = {
    "titleType":"XXX",
    "invoiceType":"1",
    "buyerName":"测试企业",
    "buyerEmail":"xxx@qq.com",
    "buyerPhone":"135xxxxxxxx",
    "remark":"",
    "items":[
        {
            "goodsCode":"",
            "goodsName":"数据服务",
            "num":2,
            "taxRate":6,
            "unit":"无",
            "taxFlag":"1",
            "amount":200,
            "mechOriginOrderNo":"1234567890"
        }
    ]
}
queryString = '' # 无查询参数时，传空字符串
url = f'https://api1.geovisearth.com/pay{path}'
nonceStr = str(uuid.uuid4())
timestamp = str(round(datetime.now().timestamp() * 1000))

payment = PaymentSign('your secretId', 'your secretKey', 'your mchid')
headers = payment.sign(path, method, body, queryString, nonceStr, timestamp)

result = payment.request(url, method, headers, body)
```