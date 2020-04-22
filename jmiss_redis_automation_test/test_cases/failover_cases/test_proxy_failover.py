#!/bin/python
# coding:utf-8

from time import sleep
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_configmap
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.steps.base_test.configmap import *
from jmiss_redis_automation_test.utils.util import get_shard_id

# 单个proxy发生failover，原地启动
def test_proxy_failover_local(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]

    oldRunTime = get_proxy_running_time(instanceId, config, proxyId)
    status = trigger_proxy_failover(config, instanceId, config["region"], proxyId)
    assert status == 200

    for i in range(0, 120):
        newRunTime = get_proxy_running_time(instanceId.config, proxyId)
        if newRunTime != oldRunTime:
            break
        sleep(1)

    assert check_admin_proxy_configmap(expected_data[flavor_id])


# 单个proxy发生failover，换机器启动
def test_proxy_failover_notLocal(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]

    oldRunTime = get_proxy_running_time(instanceId, config, proxyId)

    status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
    assert status == 200

    for i in range(0, 120):
        newRunTime = get_proxy_running_time(instanceId.config, proxyId)
        if newRunTime != oldRunTime:
            break
        sleep(1)

    assert check_admin_proxy_configmap(expected_data[flavor_id])


# 超过一半的proxy同时发生failover
def test_multi_proxy_failover(init_instance, config, expected_data):
    client, resp, instanceId = init_instance
    oldRunTimes = {}

    proxyNum = get_proxy_num(instanceId, config)
    proxyIds = get_shard_id(proxyNum, proxyNum / 2)

    for id in proxyIds:
        oldRunTimes[id] = get_proxy_running_time(instanceId, config, id)
        status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
        assert status == 200

    for id in proxyIds:
        for i in range(0, 120):
            newRunTime = get_proxy_running_time(instanceId.config, id)
            if newRunTime != oldRunTimes[id]:
                break
            sleep(1)

    assert check_admin_proxy_configmap(expected_data[flavor_id])
