from jdcloud_sdk.services.redis.apis.CreateCacheAnalysisRequest import *
from jdcloud_sdk.services.redis.apis.DescribeAnalysisTimeRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheAnalysisListRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheAnalysisResultRequest import *
from jdcloud_sdk.services.redis.apis.ModifyAnalysisTimeRequest import *

from jmiss_redis_automation_test.steps.InstanceOperation import *


def create_cache_analysis(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = CreateCacheAnalysisParameters(str(conf["region"]), instance_id)
        request = CreateCacheAnalysisRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

def query_cache_analysis_time(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeAnalysisTimeParameters(str(conf["region"]), instance_id)
        request = DescribeAnalysisTimeRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

def modify_cache_analysis_time(conf, instance_id, time, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyAnalysisTimeParameters(str(conf["region"]), instance_id, time)
        request = ModifyAnalysisTimeRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

def query_cache_analysis_list(conf, instance_id, date, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeCacheAnalysisListParameters(str(conf["region"]), instance_id, date)
        request = DescribeAnalysisTimeRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp

def query_cache_analysis_result(conf, instance_id, task_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeCacheAnalysisResultParameters(str(conf["region"]), instance_id, task_id)
        request = DescribeCacheAnalysisResultRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp