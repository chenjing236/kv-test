#!/usr/bin/python
# coding:utf-8
from InstanceOperation import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.ResetCacheInstancePasswordRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceAttributeRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceClassRequest import *
from jdcloud_sdk.services.redis.models.ConfigItem import *
from jmiss_redis_automation_test.utils.SqlConst import *


#修改缓存redis实例参数配置，支持部分参数修改
def set_config(conf, instance_id, config_list, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    instance_config = []
    for k, v in config_list.items():
        instance_config.append(ConfigItem(k, v))
    try:
        params = ModifyInstanceConfigParameters(conf["region"], instance_id, instance_config)
        request = ModifyInstanceConfigRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#查看缓存redis实例当前的配置参数
def get_config(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeInstanceConfigParameters(conf["region"], instance_id)
        request = DescribeInstanceConfigRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#重置缓存Redis实例密码，支持免密操作
def reset_password(conf, instance_id, password, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ResetCacheInstancePasswordParameters(conf["region"], instance_id)
        params.setPassword(password)
        request = ResetCacheInstancePasswordRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#修改缓存Redis实例的资源名称、描述
def reset_attribute(conf, instance_id, name=None, desc=None, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyCacheInstanceAttributeParameters(conf["region"], instance_id)
        if name is not None:
            params.setCacheInstanceName(name)
        if desc is not None:
            params.setCacheInstanceDescription(desc)
        request = ModifyCacheInstanceAttributeRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#
def reset_class(conf, instance_id, instance_class, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyCacheInstanceClassParameters(conf["region"], instance_id, instance_class)
        request = ModifyCacheInstanceClassRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp
