#!/usr/bin/python
# coding:utf-8
from InstanceOperation import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.ResetCacheInstancePasswordRequest import *

#修改缓存redis实例参数配置，支持部分参数修改
def set_config(conf, instance_id, config, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyInstanceConfigParameters(conf["region"], instance_id, config)
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
def reset_attribute(conf, instance_id, name="", desc="", client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ResetCacheInstancePasswordParameters(conf["region"], instance_id)
        request = ResetCacheInstancePasswordRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

