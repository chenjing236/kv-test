#!/bin/python
# coding:utf-8

from jmiss_redis_automation_test.utils.HttpClient import *


def generate_failover_body(instanceId, region, docker_name, type, changeIp=0):
    body = {"service": "redis", "actionName": "failover", "instanceId": instanceId,
            "requestId": str(uuid_for_request_id()),
            "region": region, "target": docker_name, "type": type, "changeIp": changeIp}
    return body


def trigger_admin_failover(config, instanceId, region):
    print ("start %s failover" % (str(instanceId) + "-admin-0"))
    body = generate_failover_body(instanceId, region, str(instanceId) + "-admin-0", "admin")
    print body
    status, _ = HttpClient.jvesselInterface(config, "POST", "/template/service_instance", body)
    return status


def trigger_proxy_failover(config, instanceId, region, id, changeIp=0):
    print ("start %s failover" % (str(instanceId) + "-proxy-" + str(id)))
    body = generate_failover_body(instanceId, region, str(instanceId) + "-proxy-" + str(id), "proxy", changeIp)
    status, _ = HttpClient.jvesselInterface(config, "POST", "/template/service_instance", body)
    return status


def trigger_redis_failover(config, instanceId, region, docker_name, changeIp=0):
    print ("start %s failover" % docker_name)
    body = generate_failover_body(instanceId, region, docker_name, "redis", changeIp)
    status, _ = HttpClient.jvesselInterface(config, "POST", "/template/service_instance", body)
    return status
