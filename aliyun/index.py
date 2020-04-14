# -*- coding: UTF-8 -*-

import time
import hmac
from os import popen
from re import search
from json import loads
from re import compile
from sys import stdout
from hashlib import sha1
from requests import get
from requests import post
from random import randint
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from json import JSONDecoder
from urllib.error import HTTPError
from datetime import datetime
from urllib.parse import quote
from base64 import encodestring
from base64 import encodebytes
from wanip import wan_ip
from dingtalk import sendmessage
from getDns import getip
from AutoEmail import Office365


def AliyunSignature(parameters):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + CharacterEncode(k) + '=' + CharacterEncode(v)
    stringToSign = 'GET&%2F&' + CharacterEncode(canonicalizedQueryString[1:])
    h = hmac.new((Aliyun_API_SECRET + "&").encode('ASCII'), stringToSign.encode('ASCII'), sha1)
    signature = encodebytes(h.digest()).strip()
    return signature


def CharacterEncode(encodeStr):
    encodeStr = str(encodeStr)
    res = quote(encodeStr.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


Aliyun_API_URL = "https://alidns.aliyuncs.com/?"
Aliyun_API_KEYID = "111111111"  # 这里为 Aliyun AccessKey 信息
Aliyun_API_SECRET = "11111111111"  # 这里为 Aliyun AccessKey 信息

Aliyun_API_RR = "ac"  # 指代二级域名
Aliyun_API_Type = "A"  # 指代记录类型


def AliyunAPIPOST(Aliyun_API_Action):
    Aliyun_API_SD = {
        'Format': 'json',  # 使用 JSON 返回数据，也可使用 XML
        'Version': '2015-01-09',  # 指定所使用的 API 版本号
        'AccessKeyId': Aliyun_API_KEYID,
        'SignatureMethod': 'HMAC-SHA1',  # 目前仅支持该算法
        'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),  # ISO8601 标准的 UTC 时间
        'SignatureVersion': '1.0',  # 签名算法版本为 1.0
        'SignatureNonce': randint(0, 99999999999999),  # 生成随机唯一数
        'Action': Aliyun_API_Action
    }
    return Aliyun_API_SD


def check_record_id():
    a = Office365()
    Aliyun_API_Post = AliyunAPIPOST('DescribeDomainRecords')
    Aliyun_API_Post['DomainName'] = 'low.im'
    Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
    Aliyun_API_Post = urlencode(Aliyun_API_Post)
    Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
    Aliyun_API_DomainRecords = '';
    try:
        Aliyun_API_DomainRecords = Aliyun_API_Request.text
    except HTTPError as e:
        print(e.code)
        print(e.read())
    result = JSONDecoder().decode(Aliyun_API_DomainRecords)  # 接受返回数据
    result = result['DomainRecords']['Record']  # 缩小数据范围
    for i in result:
        if i['RR'] == Aliyun_API_RR:
            print(i)
            msg = ' DNS解析记录:' + str(i)
            return i['RecordId']
        else:
            msg = 'DNS记录不存在'


def update_DNS():
    AC_DNS = getip('ac.123.com')
    MY_IP = wan_ip()
    a = Office365()
    if str(MY_IP) == str(AC_DNS):
        print ('WAN口DNS解析记录相同')
    else:
        Aliyun_API_Post = AliyunAPIPOST('UpdateDomainRecord')
        Aliyun_API_Post['RecordId'] = check_record_id()
        Aliyun_API_Post['RR'] = Aliyun_API_RR
        Aliyun_API_Post['Type'] = Aliyun_API_Type
        Aliyun_API_Post['Value'] = str(wan_ip())
        Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
        Aliyun_API_Post = urlencode(Aliyun_API_Post)
        Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
        print ('AC_DNS记录:' + AC_DNS + ';' + 'DNS记录:' + MY_IP + ';' + '正在更新DNS解析')
        msg = 'AC_DNS记录:' + AC_DNS + ';' + 'DNS记录:' + MY_IP + ';' + '正在更新DNS解析'



def main_handler(event, context):
    return update_DNS()
#腾讯云serverless
if __name__ == '__main__':
    update_DNS()
#
#
# def old_ip(Aliyun_API_RecordID):
#     Aliyun_API_Post = AliyunAPIPOST('DescribeDomainRecordInfo')
#     Aliyun_API_Post['RecordId'] = Aliyun_API_RecordID
#     Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
#     Aliyun_API_Post = urlencode(Aliyun_API_Post)
#     Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
#     result = JSONDecoder().decode(Aliyun_API_Request.text)
#     return result['Value']
#
#
# def add_dns(Aliyun_API_DomainIP):
#     Aliyun_API_Post = AliyunAPIPOST('AddDomainRecord')
#     Aliyun_API_Post['DomainName'] = Aliyun_API_Domain
#     Aliyun_API_Post['RR'] = Aliyun_API_RR
#     Aliyun_API_Post['Type'] = Aliyun_API_DomainType
#     Aliyun_API_Post['Value'] = Aliyun_API_DomainIP
#     Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
#     Aliyun_API_Post = urlencode(Aliyun_API_Post)
#     Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
#
#
# def delete_dns(Aliyun_API_RecordID):
#     Aliyun_API_Post = AliyunAPIPOST('DeleteDomainRecord')
#     Aliyun_API_Post['RecordId'] = Aliyun_API_RecordID
#     Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
#     Aliyun_API_Post = urlencode(Aliyun_API_Post)
#     Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
#
#
# def update_dns(Aliyun_API_RecordID, Aliyun_API_Value):
#     Aliyun_API_Post = AliyunAPIPOST('UpdateDomainRecord')
#     Aliyun_API_Post['RecordId'] = Aliyun_API_RecordID
#     Aliyun_API_Post['RR'] = Aliyun_API_RR
#     Aliyun_API_Post['Type'] = Aliyun_API_Type
#     Aliyun_API_Post['Value'] = Aliyun_API_Value
#     Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
#     Aliyun_API_Post = urlencode(Aliyun_API_Post)
#     Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)

# def set_dns(Aliyun_API_RecordID, Aliyun_API_Enabled):
#     Aliyun_API_Post = AliyunAPIPOST('SetDomainRecordStatus')
#     Aliyun_API_Post['RecordId'] = Aliyun_API_RecordID
#     Aliyun_API_Post['Status'] = "Enable" if Aliyun_API_Enabled else "Disable"
#     Aliyun_API_Post['Signature'] = AliyunSignature(Aliyun_API_Post)
#     Aliyun_API_Post = urlencode(Aliyun_API_Post)
#     Aliyun_API_Request = get(Aliyun_API_URL + Aliyun_API_Post)
