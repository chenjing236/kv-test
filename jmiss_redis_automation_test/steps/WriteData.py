#!/usr/bin/python
# coding:utf-8

import os
import random
from time import sleep

from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command
from jmiss_redis_automation_test.steps.InstanceOperation import setClient
from jmiss_redis_automation_test.steps.base_test.redis import get_used_memory

# mem_count单位是字节(B)
from jmiss_redis_automation_test.utils.HttpClient import HttpClient


def write_data(config, instance_Id, mem_count, passwd):
    usedMem = int(get_used_memory(instance_Id, config))
    if usedMem > mem_count:
        return

    resp = send_web_command(config, instance_Id, config["region"], "auth " + passwd)
    token = resp.result["token"]
    client = setClient(config)

    print("该方式压入数据过慢，建议手动使用redis-benchmark压入")

    while usedMem <= mem_count:
        string_data(config, instance_Id, token, client)
        print("memeory is used %s MB" % (usedMem / 1024 /1024))
        usedMem = int(get_used_memory(instance_Id, config))
        sleep(0.1)

    print("Data has write %s MB" % (usedMem / 1024 / 1024))


def string_data(config, instance_Id, token, client=None):
    for i in range(0, 100):
        s = random_str(50)
        data = {"type": "config", "commands": "set " + s + " " + s}
        HttpClient.underlayEntry(config, instance_Id, "POST", "/config/proxy", data)


def random_str(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt
