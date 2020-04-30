#!/usr/bin/python
# coding:utf-8
from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.Valification import assertRespNotNone
from jmiss_redis_automation_test.steps.WebCommand import *
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint


class TestWebCommand:

    @pytest.mark.webCommand
    def test_web_command(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]

        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instanceId = create_validate_instance(config, instances[0], expected_object)

        resp=send_web_command(config,instanceId,config["region"],"auth "+instances[0]["instance_password"])

        token=resp.result["token"]

        object = WebCommand(config, instanceId, config["region"], token)
        object.checkAllCommand()

