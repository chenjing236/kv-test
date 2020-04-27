#!/bin/python
# coding:utf-8

import re

from jmiss_redis_automation_test.steps.base_test.admin import get_current_rs_type
from jmiss_redis_automation_test.utils.HttpClient import *
from jmiss_redis_automation_test.utils.util import get_excepted_slots


def get_redis_flavor(instanceId, config):
    current_rs_type=str(get_current_rs_type(instanceId,config))
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId + "-master-" + current_rs_type]["flavor"]


# 返回一个list
def get_max_memory(instanceId, config):
    data = {"type": "config", "commands": "info memory"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    findResult=re.findall(r"maxmemory:(.*?)\\r\\nmax", json.dumps(resp["result"]))
    if len(set(findResult))!=1:
        raise ValueError("maxmemory is not same or find failed,%s" % findResult)
    return findResult[0]


# 返回一个list
def get_repl_backlog_size(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    findResult =re.findall(r"repl_backlog_size:(.*?)\\r\\n", json.dumps(resp))
    if len(set(findResult)) != 1:
        raise ValueError("repl_backlog_size is not same or find failed,%s" % findResult)
    return findResult[0]

# [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383'] [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383']
def get_slots(instanceId, config):
    data = {"type": "config", "commands": "slots info"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    if resp["result"]["masters"]!=resp["result"]["slaves"]:
        raise ValueError("Mismatch between master and slave")
    return resp["result"]["masters"]


# 返回一个list
def get_maxmemory_policy(instanceId, config):
    data = {"type": "config", "commands": "info memory"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    findResult=re.findall(r"maxmemory_policy:(.*?)\\r\\n", json.dumps(resp))
    if len(set(findResult))!=1:
        raise ValueError("maxmemory_policy is not same or find failed,%s" % findResult)
    return findResult[0]


# 返回ip port
def get_master_slaves(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("slave0:ip=(.*?),port", resp["result"]["masters"]), re.findall(",port=(.*?),state",
                                                                                     resp["result"]["masters"])



def get_master_aof_enabled(instanceId, config):
    data = {"type": "config", "commands": "info persistence"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    findResult =re.findall(r"aof_enabled:(.*?)\\r\\n", json.dumps(resp["result"]["masters"][0]))
    if len(set(findResult)) != 1:
        raise ValueError("master aof_enabled is not same or find failed,%s",findResult)
    return findResult[0]


# 返回两个个list
def get_slave_master(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("master_host:(.*?)\r\n", resp["result"]["slaves"][0]), re.findall("master_port:(.*?)\r\n",
                                                                                        resp["result"]["slaves"][0])



def get_slave_aof_enabled(instanceId, config):
    data = {"type": "config", "commands": "info persistence"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    findResult = re.findall(r"aof_enabled:(.*?)\\r\\n", json.dumps(resp["result"]["slaves"][0]))
    if len(set(findResult)) != 1:
        raise ValueError("slave aof_enabled is not same or find failed,%s" % findResult)
    return findResult[0]


def check_redis_param(instanceId, config, excepted, getConfigFunc):
    results = getConfigFunc(instanceId, config)
    return str(results)!=str(excepted),results


# get_slots\get_master_slaves\get_slave_master需要调用
# excepted需要是一个list
def check_redis_list(instanceId, config, excepted, getConfigFunc):
    results = getConfigFunc(instanceId, config)
    return sorted(results) != sorted(excepted),results


def check_all_redis(instanceId, config, excepted,shardNum):
    isCurrect, actual = check_redis_param(instanceId, config, excepted.redis_flavor, get_redis_flavor)
    if isCurrect:
        raise ValueError(
            "check redis_flavor error,excepted.redis_flavor=%s,actual redis_flavor=%s" % (
            excepted.redis_flavor, actual))
    isCurrect, actual = check_redis_param(instanceId, config, excepted.max_memory, get_max_memory)
    if isCurrect:
        raise ValueError(
            "check max_memory error,excepted.max_memory=%s,actual max_memory=%s" % (excepted.max_memory, actual))
    isCurrect, actual = check_redis_param(instanceId, config, excepted.repl_backlog_size, get_repl_backlog_size)
    if isCurrect:
        raise ValueError(
            "check repl_backlog_size error,excepted.repl_backlog_size=%s,actual repl_backlog_size=%s" % (
            excepted.repl_backlog_size, actual))
    isCurrect, actual = check_redis_list(instanceId, config, get_excepted_slots(shardNum), get_slots)
    if isCurrect:
        raise ValueError("check slots error,excepted.slots=%s,actual slots=%s" % (excepted.slots, actual))
    isCurrect, actual = check_redis_param(instanceId, config, excepted.maxmemory_policy, get_maxmemory_policy)
    if isCurrect:
        raise ValueError(
            "check maxmemory_policy error,excepted.maxmemory_policy=%s,actual maxmemory_policy=%s" % (
            excepted.maxmemory_policy, actual))
    '''
    isCurrect, actual = check_redis_list(instanceId, config, excepted.master_slaves, get_master_slaves)
    if isCurrect:
        raise ValueError(
            "check master_slaves error,excepted.master_slaves=%s,actual master_slaves=%s" % (excepted.master_slaves,actual))
    '''
    isCurrect, actual = check_redis_param(instanceId, config, excepted.master_aof_enabled, get_master_aof_enabled)
    if isCurrect:
        raise ValueError(
            "check master_aof_enabled error,excepted.master_aof_enabled=%s,actual master_aof_enabled=%s" % (
            excepted.master_aof_enabled, actual))
    '''
    isCurrect, actual = check_redis_list(instanceId, config, excepted.slave_master, get_slave_master)
    if isCurrect:
        raise ValueError(
            "check slave_master error,excepted.slave_master=%s,actual slave_master=%s" % (excepted.slave_master, actual))
    '''
    isCurrect, actual = check_redis_param(instanceId, config, excepted.slave_aof_enabled, get_slave_aof_enabled)
    if isCurrect:
        raise ValueError(
            "check slave_aof_enabled error,excepted.slave_aof_enabled=%s,actual slave_aof_enabled=%s" % (
            excepted.slave_aof_enabled, actual))
    return True


def get_redis_running_time(instanceId, config, replicasetName,docker_name):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][replicasetName]["containers"][docker_name][
        "running_time"]

def get_redis_ip(instanceId, config, replicasetName,docker_name):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][replicasetName]["containers"][docker_name][
        "ip"]


def get_redis_num(instanceId, config, current_rs_type):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][str(instanceId) + "-master-" + current_rs_type]["replica"]
