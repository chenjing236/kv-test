#!/bin/python
# coding:utf-8

from jmiss_redis_automation_test.utils.HttpClient import *


class configMapParam(object):
    def __init__(self, topo, proxys, status, side, current_rs_type, next_rs_type, config_param, env_max_mem,
                 is_firststart, password):
        self.topo = topo
        self.proxys = proxys
        self.status = status
        self.side = side
        self.current_rs_type = current_rs_type
        self.next_rs_type = next_rs_type
        self.config_param = config_param
        self.env_max_mem = env_max_mem
        self.is_firststart = is_firststart
        self.password = password


def get_topo(instanceId, config):
    data = {"key": "topo"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_proxys(instanceId, config):
    data = {"key": "proxys"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_status(instanceId, config):
    data = {"key": "status"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_side(instanceId, config):
    data = {"key": "side"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_current_rs_type(instanceId, config):
    data = {"key": "current_rs_type"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_next_rs_type(instanceId, config):
    data = {"key": "next_rs_type"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_config_param(instanceId, config):
    data = {"key": "configs"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_env_max_mem(instanceId, config):
    data = {"key": "envMaxMem"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_is_firststart(instanceId, config):
    data = {"key": "IsFirstStart"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_password(instanceId, config):
    data = {"key": "password_key"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def check_configmap_param(instanceId, config, excepted, getConfigFunc):
    return excepted == getConfigFunc(instanceId, config)


def check_all_configmap(instanceId, config, excepted):
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.topo, get_topo)
    if isCurrect:
        raise ValueError("check topo error,excepted.topo=%s,actual topo=%s" % excepted.topo, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.proxys, get_proxys)
    if isCurrect:
        raise ValueError("check proxys error,excepted.proxys=%s,actual proxys=%s" % excepted.proxys, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.status, get_status)
    if isCurrect:
        raise ValueError("check status error,excepted.status=%s,actual status=%s" % excepted.status, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.side, get_side)
    if isCurrect:
        raise ValueError("check side error,excepted.side=%s,actual side=%s" % excepted.side, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.current_rs_type, get_current_rs_type)
    if isCurrect:
        raise ValueError(
            "check current_rs_type error,excepted.current_rs_type=%s,actual current_rs_type=%s" % excepted.current_rs_type,
            actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.next_rs_type, get_next_rs_type)
    if isCurrect:
        raise ValueError(
            "check next_rs_type error,excepted.next_rs_type=%s,actual next_rs_type=%s" % excepted.next_rs_type, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.side, get_config_param)
    if isCurrect:
        raise ValueError(
            "check config_param error,excepted.config_param=%s,actual config_param=%s" % excepted.config_param, actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.env_max_mem, get_env_max_mem)
    if isCurrect:
        raise ValueError("check env_max_mem error,excepted.env_max_mem=%s,actual env_max_mem=%s" % excepted.env_max_mem,
                         actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.is_firststart, get_is_firststart)
    if isCurrect:
        raise ValueError(
            "check is_firststart error,excepted.is_firststart=%s,actual is_firststart=%s" % excepted.is_firststart,
            actual)
    isCurrect, actual = check_all_configmap(instanceId, config, excepted.password, get_password)
    if isCurrect:
        raise ValueError("check password error,excepted.password=%s,actual password=%s" % excepted.password, actual)

    return True
