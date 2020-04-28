#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance, wait_docker_run_time_change
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_redis_configmap
from jmiss_redis_automation_test.steps.base_test.admin import check_topo, get_docker_running_time
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint
from jmiss_redis_automation_test.steps.base_test.redis import *
from jmiss_redis_automation_test.steps.base_test.configmap import *
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestRedisFailover:
    # 单个slave发生failover，原地启动
    def test_redis_slave_failover_local(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个slave发生failover，换机器启动
    def test_redis_slave_failover_notLocal(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        oldIp = get_redis_ip(instanceId, config, replicasetName, dockerName)
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName,changeIp=1)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        newIp = get_redis_ip(instanceId, config, replicasetName, dockerName)

        assert oldIp != newIp
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 多个slave发生failover,暂定两个
    def test_multi_redis_slave_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisIds = get_shard_id(redisNum, 2)
        replicasetName = instanceId + "-slave-" + current_rs_type

        oldRunTimes = {}
        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            oldRunTimes[id] = get_docker_running_time(config,instanceId,replicasetName,dockerName)
            status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
            assert status == 200

        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            assert wait_docker_run_time_change(config, instanceId, oldRunTimes[id], replicasetName, dockerName)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个master发生failover，原地启动
    def test_redis_master_failover_local(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        sleep(30)
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个master发生failover，换机器启动
    def test_redis_master_failover_notLocal(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName,changeIp=1)
        oldIp = get_redis_ip(instanceId, config, replicasetName, dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        newIp = get_redis_ip(instanceId, config, replicasetName, dockerName)

        assert oldIp != newIp
        sleep(30)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 多个master发生failover
    def test_multi_redis_master_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisIds = get_shard_id(redisNum, 2)
        oldRunTimes = {}
        replicasetName = instanceId + "-master-" + current_rs_type

        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            oldRunTimes[id] =  get_docker_running_time(config,instanceId,replicasetName,dockerName)
            status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
            assert status == 200
        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            assert wait_docker_run_time_change(config, instanceId, oldRunTimes[id], replicasetName, dockerName)
        sleep(30)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 同分片master和slave同时发生failover,topo检查会失败
    # 这种情况需要手动人工处理
    def test_shard_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]

        replicasetMaster = instanceId + "-master-" + current_rs_type
        replicasetSlave = instanceId + "-slave-" + current_rs_type
        masterName = replicasetMaster + "-" + str(redisId)
        slaveName = replicasetSlave + "-" + str(redisId)
        oldMasterRunTime = get_docker_running_time(config, instanceId, replicasetMaster, masterName)
        oldSlaveRunTime = get_docker_running_time(config, instanceId, replicasetSlave, slaveName)

        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=masterName)
        assert status == 200
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=slaveName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldMasterRunTime, replicasetMaster, masterName)
        assert wait_docker_run_time_change(config, instanceId, oldSlaveRunTime, replicasetSlave, slaveName)

        # 等待手动运维恢复正常
        for i in range(0,3600):
            if check_topo(instanceId,config)==0:
                break
            sleep(1)

        sleep(30)
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])
