# coding=utf-8
import requests
import json
import sys, socket
import re


def wan_ip():
    url = 'http://119.29.29.29/d?dn=www.dnspod.cn&clientip=1'
    resu = requests.get(url)
    result = resu.text
    ipinfo = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", str(result))
    mess = ipinfo[1]
    return mess


if __name__ == '__main__':
    wan_ip()
