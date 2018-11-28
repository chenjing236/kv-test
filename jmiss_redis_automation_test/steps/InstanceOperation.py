#!/usr/bin/python
# coding:utf-8
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.redis.client.RedisClient import RedisClient
from jdcloud_sdk.services.redis.models.AzIdSpec import *
from jdcloud_sdk.services.redis.models.CacheInstanceSpec import *
from jdcloud_sdk.services.redis.apis.CreateCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DeleteCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstancesRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceNamesRequest import *
from jdcloud_sdk.services.redis.apis.DescribeOrderStatusRequest import *
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
    client = RedisClient(credential, gw_config, Logger(conf["logger_level"]))
    return client

def getHeader(conf):
    request_id = "req-" + str(int(time.time()))
    #测试环境header配置
    header = {'x-jdcloud-pin': str(conf["user"]), "x-jdcloud-request-id": request_id}
    #线上internal header配置
    if str(conf["header"]) == "erp":
        header = {'x-jdcloud-erp': 'duhaixing'}
    return header


def client_send(client, req):
    start_time = time.time()
    resp = client.send(req)
    end_time = time.time()
    print "[TIME] Request exec time is {0} seconds".format((end_time - start_time))
    return resp


def create_instance(conf):
    client = setClient(conf)
    header = getHeader(conf)
    instance_id = None
    resp = None
    name = "auto_test_" + str(int(time.time()))
    try:
        azId = AzIdSpec(conf["instance"]["azId"]["master"], conf["instance"]["azId"]["slave"])
        cacheInstance = CacheInstanceSpec(conf["instance"]["vpcId"], conf["instance"]["subnetId"]
                                          , conf["instance"]["cacheInstanceName"]
                                          , conf["instance"]["cacheInstanceClass"]
                                          , azId, conf["instance_password"]
                                          , conf["instance"]["cacheInstanceDescription"])
        params = CreateCacheInstanceParameters(str(conf["region"]), cacheInstance)
        charge = ChargeSpec('postpaid_by_duration', 'month', 1)
        params.setCharge(charge)
        req = CreateCacheInstanceRequest(params, header)
        resp = client_send(client, req)
        if resp.result is not None:
            instance_id = str(resp.result["cacheInstanceId"])
    except Exception, e:
        print e
    return client, resp, instance_id


def delete_instance(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DeleteCacheInstanceParameters(str(conf["region"]), instance_id)
        request = DeleteCacheInstanceRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def query_instance(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeCacheInstanceParameters(str(conf["region"]), instance_id)
        request = DescribeCacheInstanceRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def query_instance_by_id(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeCacheInstancesParameters(str(conf["region"]))
        filter_id = Filter('cacheInstanceId', [instance_id])
        filter_name = Filter('cacheInstanceName', ['automation'])
        filter_status = Filter('cacheInstanceStatus', ['running'])
        params.setFilters([filter_id, filter_name, filter_status])
        request = DescribeCacheInstancesRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#查询redis实例是否创建成功
def query_order_status(conf, request_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeOrderStatusParameters(str(conf["region"]), request_id)
        request = DescribeOrderStatusRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp



def query_instance_by_name(name, conf):
    pass

def query_instance_recurrent(wait_count, wait_time, instance_id, conf, client=None):
    if client is None:
        client = setClient(conf)
    instance = None
    while wait_count > 0:
        print "---"+str(wait_count)+"---"
        time.sleep(wait_time)
        resp = query_instance(conf, instance_id, client)
        if resp is not None and resp.result is not None:
            if resp.result["cacheInstance"]["cacheInstanceStatus"] == "running":
                instance = resp.result["cacheInstance"]
                break
        wait_count-=1
    return instance


def query_instance_names(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeInstanceNamesParameters(str(conf["region"]), instance_id)
        request = DescribeInstanceNamesRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


