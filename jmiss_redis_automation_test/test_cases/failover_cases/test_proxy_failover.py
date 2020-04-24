#!/bin/python
# coding:utf-8

from time import sleep
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_configmap
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestProxyFailover:
    # 单个proxy发生failover，原地启动
    def test_proxy_failover_local(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0])

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        oldRunTime = get_proxy_running_time(instanceId, config, proxyId)
        status = trigger_proxy_failover(config, instanceId, config["region"], proxyId)
        assert status == 200

        for i in range(0, 120):
            newRunTime = get_proxy_running_time(instanceId.config, proxyId)
            if newRunTime != oldRunTime:
                break
            sleep(1)

        assert check_admin_proxy_configmap(expected_data[instances[0]["cacheInstanceClass"]])

    # 单个proxy发生failover，换机器启动
    def test_proxy_failover_notLocal(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0])

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]

        oldRunTime = get_proxy_running_time(instanceId, config, proxyId)

        status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
        assert status == 200

        for i in range(0, 120):
            newRunTime = get_proxy_running_time(instanceId.config, proxyId)
            if newRunTime != oldRunTime:
                break
            sleep(1)

        assert check_admin_proxy_configmap(expected_data[instances[0]["cacheInstanceClass"]])

    # 超过一半的proxy同时发生failover
    def test_multi_proxy_failover(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0])

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

        assert check_admin_proxy_configmap(expected_data[instances[0]["cacheInstanceClass"]])
