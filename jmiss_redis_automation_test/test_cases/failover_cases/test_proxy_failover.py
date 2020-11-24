#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_configmap
from jmiss_redis_automation_test.steps.base_test.admin import get_docker_running_time
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestProxyFailover:
    # 单个proxy发生failover，原地启动
    def test_proxy_failover_local(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0],expected_object)

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        replicasetName = instanceId + "-proxy"
        dockerName = replicasetName + "-" + str(proxyId)
        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("proxy", config, instanceId, config["region"], id=proxyId)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        assert check_admin_proxy_configmap(instanceId,config,expected_object)

        if instanceId is not None:
            delete_instance(config, instanceId, client)

    # 单个proxy发生failover，换机器启动
    def test_proxy_failover_notLocal(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0],expected_object)

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]

        oldIp=get_proxy_ip(instanceId, config, proxyId)
        replicasetName = instanceId + "-proxy"
        dockerName = replicasetName + "-" + str(proxyId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("proxy", config, instanceId, config["region"], id=proxyId,changeIp=1)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        newIp=get_proxy_ip(instanceId, config, proxyId)

        assert oldIp!=newIp
        assert check_admin_proxy_configmap(instanceId,config,expected_object)

    # 超过一半的proxy同时发生failover
    def test_multi_proxy_failover(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0],expected_object)

        oldRunTimes = {}

        proxyNum = get_proxy_num(instanceId, config)
        proxyIds = get_shard_id(get_proxy_num(instanceId, config), proxyNum / 2)
        replicasetName = instanceId + "-proxy"

        for id in proxyIds:
            dockerName = replicasetName + "-" + str(id)
            oldRunTimes[id] = get_docker_running_time(config,instanceId,replicasetName,dockerName)
            status = trigger_docker_failover("proxy", config, instanceId, config["region"], id=id)
            assert status == 200


        for id in proxyIds:
            dockerName = replicasetName + "-" + str(id)
            assert wait_docker_run_time_change(config, instanceId, oldRunTimes[id], replicasetName, dockerName)

        assert check_admin_proxy_configmap(instanceId,config,expected_object)
