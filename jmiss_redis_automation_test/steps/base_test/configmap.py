#!/bin/python
# coding:utf-8

from jmiss_redis_automation_test.utils.HttpClient import *

def get_topo(instanceId,config):
    data = {"key":"topo"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_proxys(instanceId,config):
    data = {"key":"proxys"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_status(instanceId,config):
    data = {"key":"status"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_side(instanceId,config):
    data = {"key":"side"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_current_rs_type(instanceId,config):
    data = {"key":"current_rs_type"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_next_rs_type(instanceId,config):
    data = {"key":"next_rs_type"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

def get_config_param(instanceId,config):
    data = {"key":"configs"}
    _,_,resp=HttpClient.underlayEntry(config,instanceId,"POST","/getConfigmap",data)
    return resp["data"]

