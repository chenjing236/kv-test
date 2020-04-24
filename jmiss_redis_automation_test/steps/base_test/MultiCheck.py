#!/bin/python
# coding:utf-8
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.steps.base_test.redis import *
from jmiss_redis_automation_test.steps.base_test.configmap import *

def check_admin_proxy_redis_configmap(instanceId,config,excepted,shardNum):
    return check_all_admin(instanceId,config,excepted) and \
           check_all_redis(instanceId,config,excepted,shardNum) and \
           check_all_proxy(instanceId,config,excepted) and \
           check_all_configmap(instanceId,config,excepted)

def check_admin_proxy_configmap(instanceId,config,excepted):
    check_all_admin(instanceId,config,excepted) and \
    check_all_proxy(instanceId,config,excepted) and \
    check_all_configmap(instanceId,config,excepted)

def check_admin_configmap(instanceId,config,excepted):
    check_all_admin(instanceId,config,excepted) and \
    check_all_configmap(instanceId,config,excepted)