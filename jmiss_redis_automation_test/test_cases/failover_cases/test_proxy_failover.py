#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_configmap
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestProxyFailover:
    # 单个proxy发生failover，原地启动
    def test_proxy_failover_local(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0],expected_data)

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        oldRunTime = get_proxy_running_time(instanceId, config, proxyId)
        status = trigger_proxy_failover(config, instanceId, config["region"], proxyId)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_proxy_running_time(instanceId,config, proxyId)
                if newRunTime != oldRunTime:
                    print ("proxy failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_configmap(instanceId,config,expected_object)

    # 单个proxy发生failover，换机器启动
    @pytest.mark.proxyFailover
    def test_proxy_failover_notLocal(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0],expected_data)

        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]

        oldRunTime = get_proxy_running_time(instanceId, config, proxyId)
        oldIp=get_proxy_ip(instanceId, config, proxyId)

        status = trigger_proxy_failover(config, instanceId, config["region"], proxyId, 1)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_proxy_running_time(instanceId,config, proxyId)
                if newRunTime != oldRunTime:
                    print ("proxy failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)
        newIp=get_proxy_ip(instanceId, config, proxyId)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert oldIp!=newIp
        assert check_admin_proxy_configmap(instanceId,config,expected_object)

    # 超过一半的proxy同时发生failover
    def test_multi_proxy_failover(self, config,instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0],expected_data)

        oldRunTimes = {}

        proxyNum = get_proxy_num(instanceId, config)
        proxyIds = get_shard_id(get_proxy_num(instanceId, config), proxyNum / 2)

        for id in proxyIds:
            oldRunTimes[id] = get_proxy_running_time(instanceId, config, id)
            status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
            assert status == 200

        for id in proxyIds:
            for i in range(0, 1200):
                try:
                    newRunTime = get_proxy_running_time(instanceId,config, id)
                    if newRunTime != oldRunTimes[id]:
                        print ("proxy failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTimes[id], newRunTime))
                        break
                except ValueError as e:
                    print("except:", e)
                except KeyError as e:
                    print("except:", e)
                finally:
                    sleep(1)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_configmap(instanceId,config,expected_object)
