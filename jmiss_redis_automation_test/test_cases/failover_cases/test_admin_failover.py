#!/bin/python
# coding:utf-8

from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.base_test.MultiCheck import *
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint


class TestAdminFailover:

    @pytest.mark.adminFailover
    def test_admin_failover(self, config, instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        client, _, instanceId = create_validate_instance(config, instances[0], expected_data)

        oldRunTime = get_admin_running_time(instanceId, config)

        status = trigger_admin_failover(config, instanceId, config["region"])
        assert status == 200

        for i in range(0, 1200):
            try:
                newRunTime = get_admin_running_time(instanceId, config)
                if newRunTime != oldRunTime:
                    print ("admin failover finished,oldRunTime=%s,newRunTime=%s" % (oldRunTime, newRunTime))
                    break
            except ValueError as e:
                print("except:", e)
            finally:
                sleep(1)

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]])
        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, instances[0]["shardNumber"])
