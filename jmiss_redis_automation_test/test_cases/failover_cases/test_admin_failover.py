#!/bin/python
# coding:utf-8

from time import sleep
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.base_test.MultiTest import *
from jmiss_redis_automation_test.steps.base_test.admin import *

def test_admin_failover(init_instance, config, expected_data):
    try:
        client, resp, instanceId = init_instance

        oldRunTime = get_admin_running_time(instanceId, config)

        status = trigger_admin_failover(config, instanceId, config["region"])
        assert status == 200

        for i in range(0, 120):
            newRunTime = get_admin_running_time(instanceId.config)
            if newRunTime != oldRunTime:
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(expected_data[flavor_id])


    except ValueError as e:
        print ("except", e)