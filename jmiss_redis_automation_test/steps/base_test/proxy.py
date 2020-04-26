#!/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *


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
    return not (not resp["code"] and resp["message"] == "All proxy topology are same")


def get_password(instanceId, config):
    result = []
    data = {"type": "config", "commands": "shardsinfo"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/proxy", data)

    findResult = re.findall(r"password\\\":\\\"(.*?)\\\"", json.dumps(resp["result"]))
    if len(set(findResult)) != 1:
        raise ValueError("password is not same or find failed,%s" % findResult)
    return findResult[0]


def check_proxy_param(instanceId, config, excepted, getConfigFunc):
    actual = getConfigFunc(instanceId, config)
    return excepted != actual, actual


def check_all_proxy(instanceId, config, excepted):
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.proxy_flavor, get_proxy_flavor)
    if isCurrect:
        raise ValueError(
            "check side error,excepted.proxy_flavor=%s,actual proxy_flavor=%s" % (excepted.proxy_flavor, actual))
    '''
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.max_connection, get_max_connection)
    if isCurrect:
        raise ValueError(
            "check max_connection error,excepted.max_connection=%s,actual max_connection=%s" % (excepted.max_connection,actual))
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.flow_control, get_flow_control)
    if isCurrect:
        raise ValueError(
            "check flow_control error,excepted.flow_control=%s,actual flow_control=%s" % (excepted.flow_control, actual))
    '''
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.topo, check_topo)
    if isCurrect:
        raise ValueError("check topo error,excepted.topo=%s,actual topo=%s" % (excepted.topo, actual))
    isCurrect, actual = check_proxy_param(instanceId, config, excepted.password, get_password)
    if isCurrect:
        raise ValueError(
            "check password error,excepted.password=%s,actual password=%s" % (excepted.password, actual))
    return True


def get_proxy_running_time(instanceId, config, id):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][str(instanceId) + "-proxy"]["containers"][
        str(instanceId) + "-proxy-" + str(id)]["running_time"]

def get_proxy_ip(instanceId, config, id):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][str(instanceId) + "-proxy"]["containers"][
        str(instanceId) + "-proxy-" + str(id)]["ip"]


def get_proxy_num(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][str(instanceId) + "-proxy"]["replica"]
