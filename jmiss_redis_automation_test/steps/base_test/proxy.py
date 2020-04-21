#!/bin/python
# coding:utf-8

import re
from jmiss_redis_automation_test.utils.HttpClient import *

def get_proxy_flavor(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/getSpace")
    return resp["data"]["meta_inst"]["data"]["replicaset"][instanceId+"-proxy"]["flavor"]

# todo:接口未加
def get_max_connection(instanceId,config):
    pass

# todo:接口未加
def get_flow_control(instanceId,config):
    pass

def check_topo(instanceId,config):
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"GET","/checkTopo")
    return resp["code"]

def get_password(instanceId,config):
    result=[]
    data = {"type": "config","commands":"shardsinfo"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/config/proxy",data)
    for r in resp["result"]:
        passwds=re.findall("\"password\":\"(.*?)\"", r)
        for passwd in passwds:
            result.append(passwd)
    return result

def check_proxy_params(instanceId,config,excepted,getConfigFunc):
    return excepted==getConfigFunc(instanceId,config)