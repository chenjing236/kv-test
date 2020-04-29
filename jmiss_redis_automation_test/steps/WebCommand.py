#!/usr/bin/python
# coding:utf-8
from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command
from jmiss_redis_automation_test.steps.InstanceOperation import setClient


class WebCommand():
    def __init__(self, conf, instance_id, region, token, command, excepted_resp):
        self.conf = conf
        self.instance_id = instance_id
        self.region = region
        self.command = command
        self.excepted_resp = excepted_resp
        self.token = token
        self.client = setClient(conf)

    def set_command_exceptedResp(self, command, excepted_resp):
        self.command = command
        self.excepted_resp = excepted_resp

    def runCommand(self):
        resp = send_web_command(self.conf, self.instance_id, self.region, self.command, self.client, self.token)
        return sorted(resp.result["commandResult"]) == sorted(self.excepted_resp)


typeStringCommand = {"DEL ": "1",
                     "DUMP": ""
                     }
