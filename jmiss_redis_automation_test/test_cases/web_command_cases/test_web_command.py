#!/usr/bin/python
# coding:utf-8
from time import sleep

import pytest

from jmiss_redis_automation_test.steps.WebCommand import *
from jmiss_redis_automation_test.steps.InstanceOperation import *


class TestWebCommand:

    @pytest.mark.webCommand
    @pytest.mark.stability
    def test_web_command(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        resp=send_web_command(config,instanceId,config["region"],"auth "+instances[0]["instance_password"])
        token=resp.result["token"]
        object = WebCommand(config, instanceId, config["region"], token)
        object.checkAllCommand()

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, 1)

    @pytest.mark.webCommand
    @pytest.mark.createnobill
    def test_cli_createInstanceNobill(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]
        client, resp, instance_id = create_instance_nobill(config, instance)

        '''instance = None
        if resp.error is None and instance_id is not None:
            instance = query_instance_recurrent(200, 5, instance_id, config, client, token=True)
            config["request_id"] = resp.request_id
        else:
            config["request_id"] = ""'''

        assert instance_id is not None
        time.sleep(120)

        resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])

        token = resp.result["token"]

        object = WebCommand(config, instance_id, config["region"], token)
        object.checkAllCommand()

        if instance_id is not None:
            delete_instance(config, instance_id, client, token=True)

    @pytest.mark.webCommand
    @pytest.mark.specwebcli
    def test_specified_instance_webcli(self, config, instance_data, expected_data):
        resp = send_web_command(config, "redis-pl9nmstkrd5h", config["region"], "auth " + "1qaz2WSX")

        token = resp.result["token"]

        object = WebCommand(config, "redis-pl9nmstkrd5h", config["region"], token)
        object.checkAllCommand()



