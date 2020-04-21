#!/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *

def get_redis_flavor(instanceId,config,current_rs_type):
    _, _, resp = HttpClient.underlayEntry(config, instanceId, "GET", "/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId + "-master-"+current_rs_type]["flavor"]

# 返回一个list
def get_redis_maxmemory(instanceId,config):
    data = {"type":"config","commands":"info memory"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("maxmemory:(.*?)\r\n",resp)

# 返回一个list
def get_repl_backlog_size(instanceId,config):
    data = {"type":"config","commands":"info replication"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("repl_backlog_size:(.*?)\r\n",resp)

def get_slots(instanceId,config):
    data = {"type":"config","commands":"slots info"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return resp["result"]["masters"],resp["result"]["slaves"]
# [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383'] [u'0 2047', u'2048 4095', u'4096 6143', u'6144 8191', u'8192 10239', u'10240 12287', u'12288 14335', u'14336 16383']

# 返回一个list
def get_maxmemory_policy(instanceId,config):
    data = {"type":"config","commands":"info memory"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("maxmemory_policy:(.*?)\r\n",resp)

# 返回一个ip port
def get_master_slaves(instanceId,config):
    data = {"type":"config","commands":"info replication"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("slave0:ip=(.*?),port",resp["result"]["masters"][0]),re.findall(",port=(.*?),state",resp["result"]["masters"][0])

# 返回一个list
def get_master_aof_enabled(instanceId,config):
    data = {"type":"config","commands":"info persistence"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("aof_enabled:(.*?)\r\n",resp["result"]["masters"][0])

# 返回两个个list
def get_slave_master(instanceId,config):
    data = {"type":"config","commands":"info replication"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("master_host:(.*?)\r\n",resp["result"]["slaves"][0]),re.findall("master_port:(.*?)\r\n",resp["result"]["slaves"][0])

# 返回一个list
def get_slave_aof_enabled(instanceId,config):
    data = {"type":"config","commands":"info persistence"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/redis",data)
    return re.findall("aof_enabled:(.*?)\r\n",resp["result"]["slaves"][0])


def check_redis_params(instanceId,config,excepted,getConfigFunc):
    results=getConfigFunc(instanceId, config)
    for result in results:
        if excepted!=result:
            return False

# get_slots\get_master_slaves\get_master_slaves需要调用
# excepted需要是一个list
def check_redis_list(instanceId,config,excepted,getConfigFunc):
    results = getConfigFunc(instanceId, config)
    return sorted(results["result"]["masters"]==sorted(excepted))