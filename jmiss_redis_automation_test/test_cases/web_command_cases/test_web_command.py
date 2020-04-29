#!/usr/bin/python
# coding:utf-8
import pytest

from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command


class TestWebCommand:

    @pytest.mark.webCommand
    def test_web_command(self, config, instance_data, expected_data):
        resp=send_web_command(config,"redis-kpg04etqj51s","cn-north-1","auth 1qaz2WSX")

        print resp.result["commandResult"][0]
        print resp.result["token"]

        token=resp.result["token"]

        resp=send_web_command(config,"redis-kpg04etqj51s","cn-north-1","set kkk 123",token=token)
        print resp.result["commandResult"][0]
        assert resp.result["commandResult"][0] == "\"OK\""

        resp=send_web_command(config,"redis-kpg04etqj51s","cn-north-1","del kkk",token=token)
        print resp.result["commandResult"][0]
        assert resp.result["commandResult"][0] == 1

