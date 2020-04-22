#!/bin/python
# coding:utf-8

from jmiss_redis_automation_test.utils.HttpClient import *

def generate_failover_body(instanceId, region, docker_name, type, changeIp=0):
    return {"service": "redis",
            "actionName": "failover",
            "instanceId": instanceId,
            "requestId": str(uuid_for_request_id()),
            "region": region,
            "target": docker_name,  # 容器名称
            "type": type,  # redis，proxy, admin
            "changeIp": changeIp  # 是否换ip，0 不换，1 换，如果为1，会触发两次failover
            }

def trigger_admin_failover(config,instanceId,region):
        body=generate_failover_body(instanceId,region,str(instanceId)+"admin-0","admin")
        status,_=HttpClient.jvesselInterface(config,"POST","/template/service_instance",body)
        return status

def trigger_proxy_failover(config,instanceId,region,id,changeIp=0):
        body=generate_failover_body(instanceId,region,str(instanceId)+"proxy-"+str(id),"proxy",changeIp)
        status,_=HttpClient.jvesselInterface(config,"POST","/template/service_instance",body)
        return status

def trigger_redis_failover(config,instanceId,region,docker_name,changeIp=0):
        body=generate_failover_body(instanceId,region,docker_name,"redis",changeIp)
        status,_=HttpClient.jvesselInterface(config,"POST","/template/service_instance",body)
        return status
