#!/usr/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *


def get_side(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["side"]


def get_current_rs_type(instanceId, config):
    data = {"key": "current_rs_type"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_next_rs_type(instanceId, config):
    data = {"key": "next_rs_type"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_is_first_start(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["firstStart"]


# 返回0表示没问题
def check_topo(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/checkTopo")
    return resp["code"]


def get_password(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["topo"]["password"]


# 目前还不返回maxMem
def get_max_mempory(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["maxMem"]


def get_space_status(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getStatus")
    return resp["data"]["spaceStatus"]


def get_failovering_num(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getStatus")
    return resp["data"]["failovering"]


def get_shard_status(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    findResult = re.findall("\"status\": \"(.*?)\"", json.dumps(resp["data"]["topo"]["shards"]))
    if len(set(findResult)) != 1:
        raise ValueError("master aof_enabled is not same or find failed")
    return findResult[0]


def get_config_param(instanceId, config):
    data = {"key": "configs"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/getConfigmap", data)
    return resp["data"]


def get_admin_flavor(instanceId, config):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId + "-admin"]["flavor"]


def get_auto_backup_timer(instanceId, config):
    data = {"key": "backupschedule"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getConfigmap", data)
    return resp["data"]


def get_backup_list(instanceId, config):
    data = {"key": "backupmap"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getConfigmap", data)
    result=[]
    tmp = json.loads(resp["data"])
    for key in tmp:
        result.append(str(key))
    return result


def check_admin_param(instanceId, config, excepted, getConfigFunc):
    actual = getConfigFunc(instanceId, config)
    return str(excepted) != str(actual), actual

def check_backup_Timer(instanceId, config, excepted, getConfigFunc):
    actual = getConfigFunc(instanceId, config)
    findResult=re.findall(str(excepted),actual)
    return findResult == None, actual


def check_all_admin(instanceId, config, excepted):
    isCurrect, actual = check_admin_param(instanceId, config, excepted.side, get_side)
    if isCurrect:
        raise ValueError("check side error,excepted.side=%s,actual side=%s" % (excepted.side, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.current_rs_type, get_current_rs_type)
    if isCurrect:
        raise ValueError(
            "check current_rs_type error,excepted.current_rs_type=%s,actual current_rs_type=%s" % (
            excepted.current_rs_type, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.next_rs_type, get_next_rs_type)
    if isCurrect:
        raise ValueError(
            "check next_rs_type error,excepted.next_rs_type=%s,actual next_rs_type=%s" % (
            excepted.next_rs_type, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.is_first_start, get_is_first_start)
    if isCurrect:
        raise ValueError(
            "check is_first_start error,exceptedis_first_start=%s,actual is_first_start=%s" % (
            excepted.is_first_start, actual))
    '''
    isCurrect, actual = check_admin_param(instanceId, config, excepted.topo, check_topo)
    if isCurrect:
        raise ValueError("check topo error,excepted.topo=%s,actual topo=%s" % (excepted.topo, actual))
    isCurrect, actual = check_admin_param(instanceId, config, excepted.password, get_password)
    if isCurrect:
        raise ValueError("check password error,excepted.password=%s,actual password=%s" % (excepted.password, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.max_memory, get_max_mempory)
    if isCurrect:
        raise ValueError("check max_memory error,excepted.max_memory=%s,actual max_memory=%s" % (excepted.max_memory,actual))
    '''
    isCurrect, actual = check_admin_param(instanceId, config, excepted.space_status, get_space_status)
    if isCurrect:
        raise ValueError(
            "check space_status error,excepted.space_status=%s,actual space_status=%s" % (
            excepted.space_status, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.failovering_num, get_failovering_num)
    if isCurrect:
        raise ValueError(
            "check failovering_num error,exceptedfailovering_num=%s,actual failovering_num=%s" % (
            excepted.failovering_num, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.shard_status, get_shard_status)
    if isCurrect:
        raise ValueError(
            "check shard_status error,excepted.shard_status=%s,actual shard_status=%s" % (
            excepted.shard_status, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.config_param, get_config_param)
    if isCurrect:
        raise ValueError(
            "check config_param error,excepted.config_param=%s,actual config_param=%s" % (
            excepted.config_param, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.admin_flavor, get_admin_flavor)
    if isCurrect:
        raise ValueError(
            "check admin_flavor error,excepted.admin_flavor=%s,actual admin_flavor=%s" % (
            excepted.admin_flavor, actual))

    isCurrect, actual = check_backup_Timer(instanceId, config, excepted.auto_backup_timer, get_auto_backup_timer)
    if isCurrect:
        raise ValueError(
            "check auto_backup_timer error,excepted.auto_backup_timer=%s,actual auto_backup_timer=%s" % (
            excepted.auto_backup_timer, actual))

    isCurrect, actual = check_admin_param(instanceId, config, excepted.backup_list, get_backup_list)
    if isCurrect:
        raise ValueError(
            "check backup_list error,excepted.backup_list=%s,actual backup_list=%s" % (excepted.backup_list, actual))

    return True

def get_docker_running_time(config,instanceId,replicasetName,docker_name):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][replicasetName]["containers"][docker_name][
        "running_time"]
