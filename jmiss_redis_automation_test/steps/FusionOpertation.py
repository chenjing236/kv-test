#!/usr/bin/python
# coding:utf-8
from jdcloud_sdk.services.redis.apis.ExecuteCommandRequest import ExecuteCommandRequest, ExecuteCommandParameters

from InstanceOperation import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceConfigRequest import *
from jdcloud_sdk.services.redis.apis.ResetCacheInstancePasswordRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceAttributeRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.ModifyUserQuotaRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.DescribeUserQuotaRequest import *
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
        params = ModifyInstanceConfigParameters(str(conf["region"]), instance_id, instance_config)
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
        params = DescribeInstanceConfigParameters(str(conf["region"]), instance_id)
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
        params = ResetCacheInstancePasswordParameters(str(conf["region"]), instance_id)
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
        params = ModifyCacheInstanceAttributeParameters(str(conf["region"]), instance_id)
        if name is not None:
            params.setCacheInstanceName(name)
        if desc is not None:
            params.setCacheInstanceDescription(desc)
        request = ModifyCacheInstanceAttributeRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


# Modify cache instance by instance class and shardNumber
def reset_class(conf, instance_id, instance_class, client=None, shardNumber=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyCacheInstanceClassParameters(str(conf["region"]), instance_id, instance_class)
        if shardNumber is not None:
            params.setShardNumber(shardNumber)
        request = ModifyCacheInstanceClassRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def reset_validate_class(conf, instance_id, instance_class, client=None, shardNumber=None):
    resp = reset_class(conf, instance_id, instance_class, client, shardNumber)
    instance = query_instance_recurrent(300, 6, instance_id, conf, client)
    assert instance["cacheInstanceClass"] == instance_class


#修改规格的可见性
def reset_class_visibility(conf, class_id, type, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyInstanceClassParameters(str(conf["region"]), class_id, type)
        request = ModifyInstanceClassRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def query_class(conf, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeInstanceClassParameters(str(conf["region"]))
        params.setRedisVersion(4.0)
        request = DescribeInstanceClassRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


#修改账户的缓存Redis配额
def reset_quota(conf, quota, used, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf, True)
    resp = None
    try:
        params = ModifyUserQuotaParameters(str(conf["region"]), used, quota)
        request = ModifyUserQuotaRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp



#查询账户的缓存Redis配额信息
def query_quota(conf, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeUserQuotaParameters(str(conf["region"]))
        request = DescribeUserQuotaRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

# 发送webCommand
def send_web_command(conf,instance_id,region_id,command,client=None,token=""):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    header["webCommandtoken"]=token
    resp = None
    try:
        params=ExecuteCommandParameters(region_id,instance_id,command)
        params.setVersion("4.0")
        request=ExecuteCommandRequest(params,header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

# 去除括号中的内容
def proc_web_command_result(resps):
    result=[]
    for resp in resps:
        resp = re.sub(u"\\(.*?\\)|(.*?)\\) ", "", resp)
        resp = re.sub("\"", "", resp)
        resp = re.sub(" ", "", resp)
        result.append(resp)
    return result

def find_resp_error(resps):
    for resp in resps:
        pos=str.find("(error)",resp)
        if pos>=0:
            return False

    return True
