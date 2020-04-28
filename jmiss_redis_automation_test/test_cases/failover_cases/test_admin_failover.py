#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance, wait_docker_run_time_change
from jmiss_redis_automation_test.steps.base_test.MultiCheck import *
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint


class TestAdminFailover:

    @pytest.mark.adminFailover
    def test_admin_failover(self, config, instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        replicasetName = instanceId + "-admin"
        dockerName = replicasetName + "-0"

        oldRunTime = get_docker_running_time(config,instanceId,replicasetName,dockerName)
        status = trigger_docker_failover("admin",config,instanceId,config["region"])
        assert status == 200

        assert wait_docker_run_time_change(config,instanceId,oldRunTime,replicasetName,dockerName)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, instances[0]["shardNumber"])
