#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_redis_configmap
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint
from jmiss_redis_automation_test.steps.base_test.redis import *
from jmiss_redis_automation_test.steps.base_test.configmap import *
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestRedisFailover:
    # 单个slave发生failover，原地启动
    def test_redis_slave_failover_local(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                if newRunTime != oldRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个slave发生failover，换机器启动
    def test_redis_slave_failover_notLocal(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
        oldIp = get_redis_ip(instanceId, config, replicasetName, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName, 1)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                if newRunTime != oldRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)
        newIp = get_redis_ip(instanceId, config, replicasetName, dockerName)
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])

        assert oldIp != newIp
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 多个slave发生failover,暂定两个
    def test_multi_redis_slave_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisIds = get_shard_id(redisNum, 2)
        replicasetName = instanceId + "-slave-" + current_rs_type

        oldRunTimes = {}
        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            oldRunTimes[id] = get_redis_running_time(instanceId, config, replicasetName, dockerName)
            status = trigger_redis_failover(config, instanceId, config["region"], dockerName)
            assert status == 200

        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            for i in range(0, 1200):
                try:
                    newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                    if newRunTime != oldRunTimes[id]:
                        print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTimes[id], newRunTime))
                        break
                except ValueError as e:
                    print("except:", e)
                except KeyError as e:
                    print("except:", e)
                finally:
                    sleep(1)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个master发生failover，原地启动
    def test_redis_master_failover_local(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                if newRunTime != oldRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)
        sleep(30)
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 单个master发生failover，换机器启动
    def test_redis_master_failover_notLocal(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
        status = trigger_redis_failover(config, instanceId, config["region"],
                                        dockerName, 1)
        oldIp = get_redis_ip(instanceId, config, replicasetName, dockerName)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                if newRunTime != oldRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)

        newIp = get_redis_ip(instanceId, config, replicasetName, dockerName)

        assert oldIp != newIp
        sleep(30)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 多个master发生failover
    def test_multi_redis_master_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisIds = get_shard_id(redisNum, 2)
        oldRunTimes = {}
        replicasetName = instanceId + "-master-" + current_rs_type

        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            oldRunTimes[id] = get_redis_running_time(instanceId, config, replicasetName, dockerName)
            status = trigger_redis_failover(config, instanceId, config["region"], dockerName)
            assert status == 200
        for id in redisIds:
            dockerName = replicasetName + "-" + str(id)
            for i in range(0, 1200):
                try:
                    newRunTime = get_redis_running_time(instanceId, config, replicasetName, dockerName)
                    if newRunTime != oldRunTimes[id]:
                        print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTimes[id], newRunTime))
                        break
                except ValueError as e:
                    print("except:", e)
                except KeyError as e:
                    print("except:", e)
                finally:
                    sleep(1)
        sleep(30)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])

    # 同分片master和slave同时发生failover
    @pytest.mark.redisFailover
    def test_shard_failover(self, instance_data, config, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]

        replicasetMaster = instanceId + "-master-" + current_rs_type
        replicasetSlave = instanceId + "-slave-" + current_rs_type
        masterName = replicasetMaster + "-" + str(redisId)
        slaveName = replicasetSlave + "-" + str(redisId)
        oldMasterRunTime = get_redis_running_time(instanceId, config, replicasetMaster, masterName)
        oldSlaveRunTime = get_redis_running_time(instanceId, config, replicasetSlave, slaveName)

        status = trigger_redis_failover(config, instanceId, config["region"], masterName)
        assert status == 200
        status = trigger_redis_failover(config, instanceId, config["region"], slaveName)
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetMaster, masterName)
                if newRunTime != oldMasterRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldMasterRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)
        for i in range(0, 1200):
            try:
                newRunTime = get_redis_running_time(instanceId, config, replicasetSlave, slaveName)
                if newRunTime != oldSlaveRunTime:
                    print ("redis failover finished,oldRunTime=%s,newRunTime=%s" % (oldSlaveRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            except KeyError as e:
                print("except:", e)
            finally:
                sleep(1)

        sleep(30)
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object,
                                                 instances[0]["shardNumber"])
