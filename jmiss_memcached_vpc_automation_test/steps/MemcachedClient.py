#!/usr/bin/python
# coding:utf-8
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.memcached.client.MemcachedClient import MemcachedClient
from jdcloud_sdk.services.memcached.apis.CreateInstanceRequest import *
from jdcloud_sdk.services.memcached.models.InstanceSpec import *
from jdcloud_sdk.services.memcached.apis.DescribeInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.DescribeInstancesRequest import *
from jdcloud_sdk.services.memcached.apis.DeleteInstanceRequest import *
from jdcloud_sdk.services.charge.models.ChargeSpec import *
from jdcloud_sdk.services.common.models.Sort import *
from jdcloud_sdk.services.common.models.Filter import Filter
import time
import pytest
import logging
from jdcloud_sdk.core.logger import *
info_logger = logging.getLogger(__name__)


def setClient(conf):
    access_key = str(conf["access_key"])
    secret_key = str(conf["secret_key"])
    credential = Credential(access_key, secret_key)
    gw_config = Config(str(conf["gateway"]), SCHEME_HTTP)
    # client = MemcachedClient(credential, gw_config, Logger(ERROR))
    client = MemcachedClient(credential, gw_config)
    return client

def getHeader(conf):
    request_id = "req-" + str(int(time.time()))
    #测试环境header配置
    header = {'x-jdcloud-pin': str(conf["user"]), "x-jdcloud-request-id": request_id}
    #线上internal header配置
    if str(conf["header"]) == "erp":
        header = {'x-jdcloud-erp': 'duhaixing'}

    return header


def query_instance(name, conf):
    client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        parameters = DescribeInstancesParameters(conf["region"])
        filter1 = Filter('instanceName', name, 'eq')
        filter2 = Filter('instanceStatus', 'running')
        parameters.setFilters([filter1, filter2])
        request = DescribeInstancesRequest(parameters, header)
        resp = client.send(request)
    except Exception, e:
        print e
    return resp

def query_instance_by_name(name, conf):
    client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        parameters = DescribeInstancesParameters(conf["region"])
        filter1 = Filter('instanceName', name, 'eq')
        parameters.setFilters([filter1])
        request = DescribeInstancesRequest(parameters, header)
        resp = client.send(request)
    except Exception, e:
        print e
    return resp

def query_instance_recurrent(wait_count, wait_time, instance_name, conf):
    instance = None
    while wait_count > 0:
        print "---"+str(wait_count)+"---"
        time.sleep(wait_time)
        resp = query_instance(instance_name, conf)
        if resp is not None and resp.result is not None:
            if resp.result["totalCount"] == 1:
                instance = resp.result
                break
        wait_count-=1
    return instance


def describeInstance(client, instance_id, instance_data, conf):
    header = getHeader(conf)
    check_data = instance_data["check_data"]
    exist_data = instance_data["exist_data"]
    try:
        parameters = DescribeInstanceParameters(conf["region"], instance_id)
        request = DescribeInstanceRequest(parameters, header)
        resp = client.send(request)

    except Exception, e:
        print e

    for k, y in check_data.items():
        if k in resp.result['instance']:
            assert resp.result['instance'][k] == y
        else:
            print k, y
            assert False
    for k, y in exist_data.items():
        if k not in resp.result['instance']:
            print k,y
            assert False


def describe(client, instance_id, conf):
    header = getHeader(conf)
    resp = None
    try:
        parameters = DescribeInstanceParameters(conf["region"], instance_id)
        request = DescribeInstanceRequest(parameters, header)
        resp = client.send(request)
    except Exception, e:
        print e

    return resp

def deleteInstance(client, instance_id, conf):
    info_logger.info("[TEARDOWN] Delete the instance {0}".format(instance_id))
    header = getHeader(conf)
    try:
        parameters = DeleteInstanceParameters(conf["region"], instance_id)
        request = DeleteInstanceRequest(parameters, header)
        resp = client.send(request)
    except Exception, e:
        print e


def checkNotFound(resp):
    if resp is None or resp.error is None:
        assert False
    assert int(resp.error.code) == 404


def validateResult(result, data):
    if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
        print "type error"
        assert False
    for k, y in data.items():
        if k in result:
            assert result[k] == y
        else:
            assert False


def existResult(result, data):
    if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
        print "type error"
        return
    for k, y in data.items():
        if k not in result:
            print k, y
