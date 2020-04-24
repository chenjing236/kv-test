#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.base_test.MultiCheck import *
from jmiss_redis_automation_test.steps.base_test.admin import *


class TestAdminFailover():

    @pytest.mark.failover
    def test_admin_failover(self, config,instance_data, expected_data):
        try:
            instances = instance_data["create_cluster_specified"]
            client, _, instanceId = create_validate_instance(config, instances[0],expected_data)

            oldRunTime = get_admin_running_time(instanceId, config)

            status = trigger_admin_failover(config, instanceId, config["region"])
            assert status == 200

            for i in range(0, 120):
                newRunTime = get_admin_running_time(instanceId.config)
                if newRunTime != oldRunTime:
                    break
                sleep(1)

            assert check_admin_proxy_redis_configmap(expected_data[instances[0]["cacheInstanceClass"]],instance_data["shardNumber"])


        except ValueError as e:
            print ("except", e)
