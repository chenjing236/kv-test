#!/usr/bin/python
# coding:utf-8

from jmiss_redis_automation_test.utils.HttpClient import *

def get_side(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["side"]

def get_current_rs_type(instanceId,config):
    data = {"key":"current_rs_type"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_next_rs_type(instanceId,config):
    data = {"key":"next_rs_type"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_is_first_start(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["firstStart"]

# 返回0表示没问题
def check_topo(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/checkTopo")
    return resp["code"]

def get_password(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["password"]

# 目前还不返回maxMem
def get_max_mempory(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["maxMem"]

def get_space_status(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getStatus")
    return resp["data"]["spaceStatus"],resp["data"]["failovering"]

def get_failovering_num(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getStatus")
    return resp["data"]["spaceStatus"],resp["data"]["failovering"]

def get_shard_status(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["spaceStatus"],resp["data"]["failovering"]

def get_config_param(instanceId,config):
    data = {"key":"configs"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_admin_flavor(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId+"-admin"]["flavor"]

def get_auto_backup_timer(instanceId,config):
    data = {"key": "backupschedule"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getConfigmap",data)
    return resp["data"]

def get_backup_list(instanceId,config):
    data = {"key": "backupmap"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getConfigmap",data)
    return resp["data"]

def check_admin_params(instanceId,config,excepted,getConfigFunc):
    return excepted==getConfigFunc(instanceId,config)

