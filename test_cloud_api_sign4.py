
from datetime import datetime
import hmac
import json
import requests
import uuid
import base64
import hashlib


class CloudApiSign(object):
    def __init__(self, secretId, secretKey, serviceName, extendKeys) -> None:
        self.secretId = secretId
        self.secretKey = secretKey
        self.serviceName = serviceName
        self.extendKeys = extendKeys

    def sign(self, path, method, body, queryString, nonceStr, timestamp):
        if (body == None):
            body = ''
        else:
            body = json.dumps(body, ensure_ascii=False).replace(' ', '')

        stringToSign = self.serviceName + "\n" + method + "\n" + path + "\n" + queryString + "\n" + body + "\n" + nonceStr + "\n" + timestamp
        secretKey = base64.b64decode(self.secretKey)
        signature = hmac.new(secretKey, stringToSign.encode('utf-8'), hashlib.sha256).hexdigest()
        return {
            'Content-Type': 'application/json',
            'authorization': f'secretId={self.secretId},nonceStr={nonceStr},service={self.serviceName},timestamp={timestamp},signature={signature}{self.getExtendParam(self.extendKeys)}'
        }
    
    def request(self, url: str, method: str, headers: object, body: object|None):
        if (body == None):
            body = ''
        else:
            body = json.dumps(body, ensure_ascii=False).replace(' ', '')
        response = requests.request(method, url, headers=headers, data=body)
        return response.text

    def getExtendParam(self, extendKeys):
        result = ''
        if (extendKeys != None):
            for item in extendKeys:
                result += f',{item[0]}={item[1]}'
        return result

class PaymentSign(CloudApiSign): 
    def __init__(self, secretId, secretKey, mchid) -> None:
        super().__init__(secretId, secretKey, 'geovis-payment-center', [['mchid', mchid]])

class CertificationSign(CloudApiSign): 
    def __init__(self, secretId, secretKey) -> None:
        super().__init__(secretId, secretKey, 'geovis-certification', None)

class DataCloudSign(CloudApiSign): 
    def __init__(self, secretId, secretKey) -> None:
        super().__init__(secretId, secretKey, 'geovis-data-cloud', None)




def testGetInvoice():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v1/invoice'
    method = 'GET'
    body = None
    
    queryString = 'invoiceId=OdymJJlkJlCt5UsSfga3C-0k2jNla51W'
    url = f'https://api1.geovisearth.com/pay{path}'
    if (queryString):
        url = f'{url}?{queryString}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    payment = PaymentSign(secretId, secretKey, mchid)
    headers = payment.sign(path, method, body, queryString, nonceStr, timestamp)

    result = payment.request(url, method, headers, body)
    print('result------', result)

# testGetInvoice()

def testPostRequestInvoice():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v1/invoice'
    method = 'POST'
    body = {
        "titleType":"XXX",
        "invoiceType":"1",
        "buyerName":"测试企业",
        "buyerEmail":"yanshuo@geovis.com.cn",
        "buyerPhone":"18633849216",
        "remark":"",
        "items":[
            {
                "goodsCode":"",
                "goodsName":"数据服务1",
                "num":2,
                "taxRate":6,
                "unit":"无",
                "taxFlag":"1",
                "amount":200,
                "mechOriginOrderNo":"1234567890"
            },
            {
                "goodsCode":"444",
                "goodsName":"数据服务2",
                "num":1,
                "taxRate":3,
                "unit":"无",
                "taxFlag":"1",
                "amount":156.89,
                "mechOriginOrderNo":"1234567890123"
            },
            {
                "goodsCode":"444",
                "goodsName":"数据服务2",
                "num":1,
                "taxRate":3,
                "unit":"无",
                "taxFlag":"1",
                "amount":166,
                "mechOriginOrderNo":"123456789012345"
            }
        ]
    }
    queryString = ''
    url = f'https://api1.geovisearth.com/pay{path}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    payment = PaymentSign(secretId, secretKey, mchid)
    headers = payment.sign(path, method, body, queryString, nonceStr, timestamp)

    result = payment.request(url, method, headers, body)
    print('result---post---', result)

# testPostRequestInvoice()

def testGetOrderDetail():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v2/access/orderDetail'
    method = 'GET'
    body = None
    
    queryString = 'orderNo=m6fDXG8v87liqXJBGh38tq1h7Jrv1Uui'
    url = f'https://api1.geovisearth.com/pay{path}'
    if (queryString):
        url = f'{url}?{queryString}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    payment = PaymentSign(secretId, secretKey, mchid)
    headers = payment.sign(path, method, body, queryString, nonceStr, timestamp)

    result = payment.request(url, method, headers, body)
    print('testGetOrderDetail------', result)

# testGetOrderDetail()


def testPrepayOrder():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v2/access/prepay'
    method = 'POST'
    body = {
        'orderNo': 'test_2024092500001111',
        'productName': '测试商品',
        'total': 1,
        'payMode': 'wxpay',
        'payChannel': 'NATIVE',
        'callbackUrl': 'http://www.baidu.com?ad=12',
        'userId': 'test_userid_xxxxxxxx_yyyyyyyyyyyyy'
    }
    
    queryString = ''
    url = f'https://api1.geovisearth.com/pay{path}'
    if (queryString):
        url = f'{url}?{queryString}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    payment = PaymentSign(secretId, secretKey, mchid)
    headers = payment.sign(path, method, body, queryString, nonceStr, timestamp)

    result = payment.request(url, method, headers, body)
    print('result------', result)

# testPrepayOrder()


def testGetCertification():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v1/cloudapi/certification/industry'
    method = 'GET'
    body = None
    
    # queryString = 'phone=13552403690&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1NzMyOGIwLTgwOTctNDUwYi1iYzI0LWRjZTBjYjFjY2ExMyIsImV4cCI6MTcyOTg0NzIwNywiaXNzIjoic3NvLmdlb3Zpc2VhcnRoLmNvbSJ9.skx9Qm_xubCllIIvbd6_UwUDRSWZO5z_sUMtydHX6s4&appkey=7C31B18286A649B792AEC49062DAAB22'
    queryString = ''
    url = f'https://api1-dev.geovisearth.com/daas/certification-dev{path}'
    if (queryString):
        url = f'{url}?{queryString}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    cert = CertificationSign(secretId, secretKey)
    headers = cert.sign(path, method, body, queryString, nonceStr, timestamp)

    result = cert.request(url, method, headers, body)
    print('testGetCertification------', result)

# testGetCertification()


def testGetUserAbout():
    secretId = 'sCx7-dtUrZQIQY5Zvkkn3TVALrU'
    secretKey = '9Q1LxWRiRnmO0cb/k25ZndKP7q76bAxt6vIY40Q/OHI7GiSbTJkgZCLL4+kLGK8yRjpj13g12f5/Y7zdunxuKg=='
    mchid = 'QV5MGMKCM7MBAE1WZKFHKQTK'
    path = '/v1/cloudapi/application/publics'
    method = 'GET'
    body = None
    
    queryString = 'mobile=13552403690&channel=xx'
    # queryString = ''
    url = f'https://datacloud1.geovisearth.com{path}'
    if (queryString):
        url = f'{url}?{queryString}'
    nonceStr = str(uuid.uuid4())
    timestamp = str(round(datetime.now().timestamp() * 1000))

    dataCloudSign = DataCloudSign(secretId, secretKey)
    headers = dataCloudSign.sign(path, method, body, queryString, nonceStr, timestamp)

    result = dataCloudSign.request(url, method, headers, body)
    print('testGetUserAbout---', result)

# testGetUserAbout()