#!/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *


class proxyParam(object):
    def __init__(self, proxy_flavor, max_connection, flow_control, topo, password):
        self.proxy_flavor = proxy_flavor
        self.max_connection = max_connection
        self.flow_control = flow_control
        self.topo = topo
        self.password = password


def get_proxy_flavor(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId + "-proxy"]["flavor"]


# todo:接口未加
def get_max_connection(instanceId, config):
    pass


# todo:接口未加
def get_flow_control(instanceId, config):
    pass

# 返回True表示成功
def check_topo(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getProxyTopo")
    return not resp["code"] and resp["message"]=="All proxy topology are same"


def get_password(instanceId, config):
    result = []
    data = {"type": "config", "commands": "shardsinfo"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/proxy", data)
    for r in resp["result"]:
        passwds = re.findall("\"password\":\"(.*?)\"", r)
        for passwd in passwds:
            result.append(passwd)
    return result


def check_proxy_param(instanceId, config, excepted, getConfigFunc):
    return excepted == getConfigFunc(instanceId, config)


def check_all_proxy(instanceId, config, excepted):
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.proxy_flavor, get_proxy_flavor)
    if not isCurrect:
        raise ValueError("check side error,excepted.side=%s,actual side=%s" % excepted.side, actual)
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.max_connection, get_max_connection)
    if not isCurrect:
        raise ValueError(
            "check max_connection error,excepted.max_connection=%s,actual max_connection=%s" % excepted.max_connection,
            actual)
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.flow_control, get_flow_control)
    if not isCurrect:
        raise ValueError(
            "check flow_control error,excepted.flow_control=%s,actual flow_control=%s" % excepted.flow_control, actual)
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.topo, check_topo)
    if not isCurrect:
        raise ValueError("check topo error,excepted.topo=%s,actual topo=%s" % excepted.topo, actual)
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.password, get_password)
    if not isCurrect:
        raise ValueError("check password error,excepted.password=%s,actual password=%s" % excepted.password, actual)
    return True
