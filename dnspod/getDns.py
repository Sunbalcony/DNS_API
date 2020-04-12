import json
import sys, socket
import re


def getip(oneDomain):
    result = socket.getaddrinfo(oneDomain, None)
    listip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", str(result))
    addr = listip[0]
    return addr


if __name__ == '__main__':
    getip()
