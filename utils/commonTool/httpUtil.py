# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

import requests
from utils.commonTool.configUtil import ConfigUtil
from utils.log.mylog import MyLogger

log = MyLogger()


class HttpUtil(object):
    global headers
    log.info("设置Http请求头信息")
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Connection": "Keep-Alive",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    @classmethod
    def get(cls, confSection="bdd-Interface", confFile="\\config\\buydodoInterface.yml", data=None, json=None,
            **kwargs):
        host = ConfigUtil.get("bdd-Interface", option='Host', path=confFile)
        # port = ConfigUtil.get(confSection, 'Port', confFile)
        path = ConfigUtil.get(confSection, option='Path', path=confFile)
        url = host + path
        log.info("get请求地址为%s" % url)
        response = requests.get(url, data=data, json=json, headers=headers, **kwargs)
        log.info("请求返回数据为%s" % response)
        response.raise_for_status()
        return response.json()

    @classmethod
    def post(cls, confSection="bdd-Interface", confFile="\\config\\buydodoInterface.yml", data=None,
             json=None, **kwargs):
        host = ConfigUtil.get("bdd-Interface", option='Host', path=confFile)
        # port = ConfigUtil.get(confSection, 'Port', confFile)
        path = ConfigUtil.get(confSection, option='Path', path=confFile)
        url = host + path
        log.info("post请求地址为%s" % url)
        response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
        log.info("请求返回数据为%s" % response)
        response.raise_for_status()
        return response.json()

# http = HttpUtil.post(confSection="payOrder-Interface",
#                      data="orderId=15215395040002")
# print(http)
