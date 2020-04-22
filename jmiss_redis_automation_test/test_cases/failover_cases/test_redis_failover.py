#!/bin/python
# coding:utf-8

from time import sleep
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.base_test.MultiTest import check_admin_proxy_redis_configmap
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.redis import *
from jmiss_redis_automation_test.steps.base_test.configmap import *
from jmiss_redis_automation_test.utils.util import get_shard_id

# 单个slave发生failover，原地启动
def test_redis_slave_failover_local(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisId = get_shard_id(redisNum, 1)[0]
    current_rs_type = get_current_rs_type(instanceId, config)
    dockerName = instanceId + "-slave-" + current_rs_type + "-" + str(redisId)

    oldRunTime = get_redis_running_time(instanceId, config, dockerName)
    status = trigger_redis_failover(config, instanceId, config["region"],
                                    dockerName)
    assert status == 200

    for i in range(0, 120):
        newRunTime = get_redis_running_time(instanceId.config, dockerName)
        if newRunTime != oldRunTime:
            break
        sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])


# 单个slave发生failover，换机器启动
def test_redis_slave_failover_notLocal(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisIds = get_shard_id(redisNum, 1)[0]
    current_rs_type = get_current_rs_type(instanceId, config)
    oldRunTimes = {}

    for id in redisIds:
        dockerName = instanceId + "-slave-" + current_rs_type + "-" + str(id)
        oldRunTimes[id] = get_redis_running_time(instanceId, config, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName, 1)
        assert status == 200

    for id in redisIds:
        dockerName = instanceId + "-slave-" + current_rs_type + "-" + str(id)
        for i in range(0, 120):
            newRunTime = get_redis_running_time(instanceId.config, dockerName)
            if newRunTime != oldRunTimes[id]:
                break
            sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])


# 多个slave发生failover
def test_multi_redis_slave_failover(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisIds = get_shard_id(redisNum, 2)
    current_rs_type = get_current_rs_type(instanceId, config)
    oldRunTimes={}

    for id in redisIds:
        dockerName = instanceId + "-slave-" + current_rs_type + "-" + str(id)
        oldRunTimes[id] = get_redis_running_time(instanceId, config, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"], dockerName, 1)
        assert status == 200
    for id in redisIds:
        for i in range(0, 120):
            newRunTime = get_redis_running_time(instanceId, config, dockerName)
            if newRunTime != oldRunTimes[id]:
                break
            sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])

# 单个master发生failover，原地启动
def test_redis_master_failover_local(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisId = get_shard_id(redisNum, 1)[0]
    current_rs_type = get_current_rs_type(instanceId, config)
    dockerName = instanceId + "-master-" + current_rs_type + "-" + str(redisId)

    oldRunTime = get_redis_running_time(instanceId, config, dockerName)
    status = trigger_redis_failover(config, instanceId, config["region"],
                                    dockerName)
    assert status == 200

    for i in range(0, 120):
        newRunTime = get_redis_running_time(instanceId.config, dockerName)
        if newRunTime != oldRunTime:
            break
        sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])


# 单个master发生failover，换机器启动
def test_redis_master_failover_notLocal(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisIds = get_shard_id(redisNum, 1)[0]
    current_rs_type = get_current_rs_type(instanceId, config)
    oldRunTimes = {}

    for id in redisIds:
        dockerName = instanceId + "-master-" + current_rs_type + "-" + str(id)
        oldRunTimes[id] = get_redis_running_time(instanceId, config, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName, 1)
        assert status == 200

    for id in redisIds:
        dockerName = instanceId + "-slave-" + current_rs_type + "-" + str(id)
        for i in range(0, 120):
            newRunTime = get_redis_running_time(instanceId.config, dockerName)
            if newRunTime != oldRunTimes[id]:
                break
            sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])


# 多个master发生failover
def test_multi_redis_master_failover(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisIds = get_shard_id(redisNum, 2)
    current_rs_type = get_current_rs_type(instanceId, config)
    oldRunTimes = {}

    for id in redisIds:
        dockerName = instanceId + "-master-" + current_rs_type + "-" + str(id)
        oldRunTimes[id] = get_redis_running_time(instanceId, config, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"], dockerName, 1)
        assert status == 200
    for id in redisIds:
        for i in range(0, 120):
            newRunTime = get_redis_running_time(instanceId, config, dockerName)
            if newRunTime != oldRunTimes[id]:
                break
            sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])

# 同分片master和slave同时发生failover
def test_shard_failover(init_instance, config, expected_data):
    client, resp, instanceId = init_instance

    redisNum = get_redis_num(instanceId, config)
    redisId = get_shard_id(redisNum, 1)
    current_rs_type = get_current_rs_type(instanceId, config)

    masterName=instanceId + "-master-" + current_rs_type + "-" + str(redisId)
    slaveName = instanceId + "-slave-" + current_rs_type + "-" + str(redisId)

    oldMasterRunTime=get_redis_running_time(instanceId, config, masterName)
    oldSlaveRunTime = get_redis_running_time(instanceId, config, slaveName)

    status = trigger_redis_failover(config, instanceId, config["region"], masterName, 1)
    assert status == 200

    status = trigger_redis_failover(config, instanceId, config["region"], slaveName, 1)
    assert status == 200

    for i in range(0, 120):
        newRunTime = get_redis_running_time(instanceId, config, masterName)
        if newRunTime != oldMasterRunTime:
            break
        sleep(1)

    for i in range(0, 120):
        newRunTime = get_redis_running_time(instanceId, config, slaveName)
        if newRunTime != oldSlaveRunTime:
            break
        sleep(1)

    assert check_admin_proxy_redis_configmap(expected_data[flavor_id])