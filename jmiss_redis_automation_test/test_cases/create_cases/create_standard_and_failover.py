#!/bin/python
# coding:utf-8
import time

from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.utils.util import *


class TestCreateStandardFailover:

    # admin发生failover及基本点验证
    @staticmethod
    def __admin_failover_validation(config, instance, expected_object, instance_id):
        # admin failover trigger
        replicasetName = instance_id + "-admin"
        dockerName = replicasetName + "-0"
        oldRunTime = get_docker_running_time(config, instance_id, replicasetName, dockerName)
        status = trigger_docker_failover("admin", config, instance_id, config["region"])
        assert status == 200
        assert wait_docker_run_time_change(config, instance_id, oldRunTime, replicasetName, dockerName)

        # base validation
        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["shardNumber"])

    # 单个proxy发生failover
    @staticmethod
    def __proxy_failover_validation(config, expected_object, instance_id):
        # proxy failover trigger
        proxyId = get_shard_id(get_proxy_num(instance_id, config), 1)[0]
        replicasetName = instance_id + "-proxy"
        dockerName = replicasetName + "-" + str(proxyId)
        oldRunTime = get_docker_running_time(config, instance_id, replicasetName, dockerName)
        status = trigger_docker_failover("proxy", config, instance_id, config["region"], id=proxyId)
        assert status == 200
        assert wait_docker_run_time_change(config, instance_id, oldRunTime, replicasetName, dockerName)

        # base validation
        assert check_admin_proxy_configmap(instance_id, config, expected_object)

    # 单个Redis master 发生failover
    @staticmethod
    def __master_failover_validation(config, instance, expected_object, instance_id):
        # master failover trigger
        current_rs_type = get_current_rs_type(instance_id, config)
        redisNum = get_redis_num(instance_id, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instance_id + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instance_id, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instance_id, config["region"], docker_name=dockerName)
        assert status == 200
        assert wait_docker_run_time_change(config, instance_id, oldRunTime, replicasetName, dockerName)

        time.sleep(30)
        # base validation
        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["shardNumber"])

    # 单个redis slave 发生failover
    @staticmethod
    def __slave_failover_validation(config, instance, expected_object, instance_id):
        # slave failover trigger
        current_rs_type = get_current_rs_type(instance_id, config)
        redisNum = get_redis_num(instance_id, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instance_id + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instance_id, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instance_id, config["region"], docker_name=dockerName)
        assert status == 200
        assert wait_docker_run_time_change(config, instance_id, oldRunTime, replicasetName, dockerName)

        # base validation
        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["shardNumber"])

    # 所有节点同时发生failover
    @staticmethod
    def __all_nodes_failover_validation(config, instance, expected_object, instance_id):
        current_rs_type = get_current_rs_type(instance_id, config)
        redisNum = get_redis_num(instance_id, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]

        replicasetMaster = instance_id + "-master-" + current_rs_type
        replicasetSlave = instance_id + "-slave-" + current_rs_type
        masterName = replicasetMaster + "-" + str(redisId)
        slaveName = replicasetSlave + "-" + str(redisId)
        proxyId = get_shard_id(get_proxy_num(instance_id, config), 1)[0]
        replicasetName = instance_id + "-proxy"
        dockerName = replicasetName + "-" + str(proxyId)
        oldMasterRunTime = get_docker_running_time(config, instance_id, replicasetMaster, masterName)
        oldSlaveRunTime = get_docker_running_time(config, instance_id, replicasetSlave, slaveName)
        oldRunTime = get_docker_running_time(config, instance_id, replicasetName, dockerName)

        status = trigger_docker_failover("redis", config, instance_id, config["region"], docker_name=masterName)
        assert status == 200
        status = trigger_docker_failover("redis", config, instance_id, config["region"], docker_name=slaveName)
        assert status == 200
        status = trigger_docker_failover("proxy", config, instance_id, config["region"], id=proxyId)
        assert status == 200

        assert wait_docker_run_time_change(config, instance_id, oldMasterRunTime, replicasetMaster, masterName)
        assert wait_docker_run_time_change(config, instance_id, oldSlaveRunTime, replicasetSlave, slaveName)
        assert wait_docker_run_time_change(config, instance_id, oldRunTime, replicasetName, dockerName)

        # 等待手动运维恢复正常
        for i in range(0, 3600):
            if check_topo(instance_id, config) == 0:
                break
            time.sleep(1)

        time.sleep(30)
        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["shardNumber"])


    # 挑个1G主从版本即可

    ## 有密码实例
    # admin发生failover
    # 单个proxy发生failover
    # 单个Redis master 发生failover
    # 单个redis slave 发生failover
    # 所有节点同时发生failover
    def test_standard_failover_with_psw(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]
        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]], instance["instance_password"])

        client, resp, instance_id = create_instance_with_data(config, instance, expected_data)
        self.__admin_failover_validation(config, instance, expected_object, instance_id)
        self.__proxy_failover_validation(config, expected_object, instance_id)
        self.__master_failover_validation(config, instance, expected_object, instance_id)
        self.__slave_failover_validation(config, instance, expected_object, instance_id)
        self.__all_nodes_failover_validation(config, instance, expected_object, instance_id)

        if instance_id is not None:
            delete_instance(config, instance_id, client)


    ## 无密码实例
    # admin发生failover
    # 单个proxy发生failover
    # 单个Redis master 发生failover
    # 单个redis slave 发生failover
    # 所有节点同时发生failover
    def test_standard_failover_without_psw(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][1]
        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]], instance["instance_password"])

        client, resp, instance_id = create_instance_with_data(config, instance, expected_data)
        self.__admin_failover_validation(config, instance, expected_object, instance_id)
        self.__proxy_failover_validation(config, expected_object, instance_id)
        self.__master_failover_validation(config, instance, expected_object, instance_id)
        self.__slave_failover_validation(config, instance, expected_object, instance_id)
        self.__all_nodes_failover_validation(config, instance, expected_object, instance_id)

        if instance_id is not None:
            delete_instance(config, instance_id, client)
