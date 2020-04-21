#!/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *


class redisParam(object):
    def __init__(self, redis_flavor, redis_maxmemory, repl_backlog_size, slots, maxmemory_policy, master_slaves,
                 master_aof_enabled, slave_master, slave_aof_enabled):
        self.redis_flavor = redis_flavor
        self.redis_maxmemory = redis_maxmemory
        self.repl_backlog_size = repl_backlog_size
        self.slots = slots
        self.maxmemory_policy = maxmemory_policy
        self.master_slaves = master_slaves
        self.master_aof_enabled = master_aof_enabled
        self.slave_master = slave_master
        self.slave_aof_enabled = slave_aof_enabled


def get_redis_flavor(instanceId, config, current_rs_type):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId + "-master-" + current_rs_type]["flavor"]


# 返回一个list
def get_redis_maxmemory(instanceId, config):
    data = {"type": "config", "commands": "info memory"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("maxmemory:(.*?)\r\n", resp)


# 返回一个list
def get_repl_backlog_size(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("repl_backlog_size:(.*?)\r\n", resp)


def get_slots(instanceId, config):
    data = {"type": "config", "commands": "slots info"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return resp["result"]["masters"], resp["result"]["slaves"]


# [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383'] [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383']

# 返回一个list
def get_maxmemory_policy(instanceId, config):
    data = {"type": "config", "commands": "info memory"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("maxmemory_policy:(.*?)\r\n", resp)


# 返回一个ip port
def get_master_slaves(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("slave0:ip=(.*?),port", resp["result"]["masters"][0]), re.findall(",port=(.*?),state",
                                                                                        resp["result"]["masters"][0])


# 返回一个list
def get_master_aof_enabled(instanceId, config):
    data = {"type": "config", "commands": "info persistence"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("aof_enabled:(.*?)\r\n", resp["result"]["masters"][0])


# 返回两个个list
def get_slave_master(instanceId, config):
    data = {"type": "config", "commands": "info replication"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("master_host:(.*?)\r\n", resp["result"]["slaves"][0]), re.findall("master_port:(.*?)\r\n",
                                                                                        resp["result"]["slaves"][0])


# 返回一个list
def get_slave_aof_enabled(instanceId, config):
    data = {"type": "config", "commands": "info persistence"}
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "POST", "/config/redis", data)
    return re.findall("aof_enabled:(.*?)\r\n", resp["result"]["slaves"][0])


def check_redis_param(instanceId, config, excepted, getConfigFunc):
    results = getConfigFunc(instanceId, config)
    for result in results:
        if excepted != result:
            return False


# get_slots\get_master_slaves\get_slave_master需要调用
# excepted需要是一个list
def check_redis_list(instanceId, config, excepted, getConfigFunc):
    results = getConfigFunc(instanceId, config)
    return sorted(results["result"]["masters"] == sorted(excepted))


def check_all_admin(instanceId, config, excepted):
    isCurrect, actual = check_redis_param(instanceId, config, excepted.redis_flavor, get_redis_flavor)
    if isCurrect:
        raise ValueError(
            "check redis_flavor error,excepted.redis_flavor=%s,actual redis_flavor=%s" % excepted.redis_flavor, actual)
    isCurrect, actual = check_redis_param(instanceId, config, excepted.redis_maxmemory, get_redis_maxmemory)
    if isCurrect:
        raise ValueError(
            "check redis_maxmemory error,excepted.redis_maxmemory=%s,actual redis_maxmemory=%s" % excepted.redis_maxmemory,
            actual)
    isCurrect, actual = check_redis_param(instanceId, config, excepted.repl_backlog_size, get_repl_backlog_size)
    if isCurrect:
        raise ValueError(
            "check repl_backlog_size error,excepted.repl_backlog_size=%s,actual repl_backlog_size=%s" % excepted.repl_backlog_size,
            actual)
    isCurrect, actual = check_redis_list(instanceId, config, excepted.slots, get_slots)
    if isCurrect:
        raise ValueError("check slots error,excepted.slots=%s,actual slots=%s" % excepted.slots, actual)
    isCurrect, actual = check_redis_param(instanceId, config, excepted.maxmemory_policy, get_maxmemory_policy)
    if isCurrect:
        raise ValueError(
            "check maxmemory_policy error,excepted.maxmemory_policy=%s,actual maxmemory_policy=%s" % excepted.maxmemory_policy,
            actual)
    isCurrect, actual = check_redis_list(instanceId, config, excepted.master_slaves, get_master_slaves)
    if isCurrect:
        raise ValueError(
            "check master_slaves error,excepted.master_slaves=%s,actual master_slaves=%s" % excepted.master_slaves,
            actual)
    isCurrect, actual = check_redis_param(instanceId, config, excepted.master_aof_enabled, get_master_aof_enabled)
    if isCurrect:
        raise ValueError(
            "check master_aof_enabled error,excepted.master_aof_enabled=%s,actual master_aof_enabled=%s" % excepted.master_aof_enabled,
            actual)
    isCurrect, actual = check_redis_list(instanceId, config, excepted.slave_master, get_slave_master)
    if isCurrect:
        raise ValueError(
            "check slave_master error,excepted.slave_master=%s,actual slave_master=%s" % excepted.slave_master, actual)
    isCurrect, actual = check_redis_param(instanceId, config, excepted.slave_aof_enabled, get_slave_aof_enabled)
    if isCurrect:
        raise ValueError(
            "check slave_aof_enabled error,excepted.slave_aof_enabled=%s,actual slave_aof_enabled=%s" % excepted.slave_aof_enabled,
            actual)
    return True
