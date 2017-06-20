#!/usr/bin/env python3

# Usage: ./reset_eap330.py USERNAME PASSWORD IP_ADDRESS

import requests
import hashlib
import sys

username = sys.argv[1]
password = sys.argv[2].encode('utf-8')
ip = sys.argv[3]

passwordMD5 = hashlib.md5(password).hexdigest().upper()
header_firefox = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://" + ip + "/",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
                }

session = requests.session()
response = session.get("http://{}/data/login.json".format(ip))
dutMode = response.json()["dutMode"]
assert(dutMode == "EAP330")
login_data = {"username": username, "password": passwordMD5}
response = session.post("http://{}/".format(ip), login_data)
assert(response.ok)
response = session.get("http://{}/data/configReboot.json".format(ip), headers=header_firefox)
assert response.json()["success"]
assert response.json()["process"] == "reboot"
print("ok")
