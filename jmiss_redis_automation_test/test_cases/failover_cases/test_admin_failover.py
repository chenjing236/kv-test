#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import assertRespNotNone
from jmiss_redis_automation_test.utils.util import get_sha256_pwd


class TestAdminFailover:
    @pytest.mark.regression
    def test_admin_failover(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        replicasetName = instanceId + "-admin"
        dockerName = replicasetName + "-0"

        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("admin",config,instanceId,config["region"])
        assert status == 200

        assert wait_docker_run_time_change(config,instanceId,oldRunTime,replicasetName,dockerName)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, instances[0]["shardNumber"])

        if instanceId is not None:
            delete_instance(config, instanceId, client)

    @pytest.mark.adminFailover
    def test_modify_passwd_and_admin_failover(self, config, instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        # 修改密码
        newPasswd="2qaz2WSX"
        resp = reset_password(config, instanceId, newPasswd, client)
        assertRespNotNone(resp)
        expected_object.password=get_sha256_pwd(newPasswd)

        replicasetName = instanceId + "-admin"
        dockerName = replicasetName + "-0"

        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("admin", config, instanceId, config["region"])
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, instances[0]["shardNumber"])

        print "admin failover success"
        sleep(10)

        # 第二次修改密码并触发admin failover
        newPasswd = "3qaz2WSX"
        resp = reset_password(config, instanceId, newPasswd, client)
        assertRespNotNone(resp)
        expected_object.password = get_sha256_pwd(newPasswd)

        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("admin", config, instanceId, config["region"])
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, instances[0]["shardNumber"])

        print "admin failover success"



