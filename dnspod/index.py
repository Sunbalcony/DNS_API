import base64
import hashlib
import hmac
import json
import random
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen
from wanip import wan_ip
from dingtalk import sendmessage

host = 'cns.api.qcloud.com/v2/index.php'
secret_id = "xxx"
secret_key = "xxxx"


def request(action, region=None, dict_arg=None, **kw_arg):
    params = dict(dict_arg) if dict_arg is not None else {}
    params.update(kw_arg)

    # 公共参数
    params['Action'] = action
    if region is not None:
        params['Region'] = region
    params['Timestamp'] = int(datetime.timestamp(datetime.now()))
    params['Nonce'] = random.randint(1, 2 ** 16 - 1)
    params['SecretId'] = secret_id
    params['SignatureMethod'] = 'HmacSHA256'
    params = {str(k): str(v) for k, v in params.items()}

    # 签名原文字符串
    text = 'GET' + host + '?' + '&'.join(k + '=' + v for k, v in sorted(params.items()))
    # 加密
    signature = hmac.new(secret_key.encode(), text.encode(), hashlib.sha256).digest()
    # base64编码并添加到参数列表中
    params['Signature'] = base64.b64encode(signature).decode()

    # 生成url，参数中可能会有特殊字符，所以需要urlencode
    url = 'https://' + host + '?' + urlencode(sorted(params.items()))
    # 发出请求
    contents = json.loads(urlopen(url).read().decode('unicode-escape'))
    # 校验是否成功
    if contents['code'] != 0:
        raise Exception(contents['message'])
    # 返回数据
    print (contents['data'])
    return contents['data']


records = request('RecordList', domain="shy.pet")['records']
for record in records:
    # 找到对应的记录值
    if record['name'] == 'ns':
        # 如果有修改的必要的话
        my_ip = wan_ip()
        print ("我的IP是" + my_ip)
        if record['value'] != my_ip:
            # 在原记录值的基础上修改
            print ("需要修改")
            result = request('RecordModify',
                             domain="shy.pet",
                             recordId=record['id'],
                             subDomain=record['name'],
                             recordType=record['type'],
                             recordLine=record['line'],
                             value=my_ip,
                             ttl=record['ttl'],
                             mx=record['mx'])
            sendmessage("WANIP:" + my_ip + "正在同步DNS解析" + str(result))
        else:
            sendmessage("WANIP:" + my_ip + "DNS记录:" + record['value'] + "无需同步DNS解析")
