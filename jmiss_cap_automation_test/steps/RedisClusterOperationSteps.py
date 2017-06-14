# -*- coding: utf-8 -*-

import json
import logging
import time
from business_function.RedisCap import *

logger_info = logging.getLogger(__name__)


# 创建缓存云实例，创建接口返回request id
def create_redis_instance_step(redis_cap):
    res_data = redis_cap.create_instance()
    request_id = res_data["requestId"]
    # if res_data["code"] is not None:
    #     error_msg = res_data["message"]
    #     logger_info.error("[ERROR] It is failed to create a redis, error message is [%s]", error_msg)
    #     assert False, "[ERROR] It is failed to create a redis, error message is {0}".format(error_msg)
    return request_id


# 创建包年包月缓存云实例，创建接口返回request id
def create_redis_month_instance_step(redis_cap):
    res_data = redis_cap.create_month_instance()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a redis, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a redis, error message is {0}".format(error_msg)
    return request_id


# 查询云缓存实例详情
def query_cache_cluster_detail_step(redis_cap, cluster_id):
    res_data = redis_cap.query_cache_cluster_detail(cluster_id)
    # request_id = res_data["requestId"]
    billing_order = res_data["billingOrder"]
    cluster = res_data["cluster"]
    return billing_order, cluster


# 删除redis资源
def delete_redis_instance_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_cache_cluster(cluster_id)
    request_id = res_data["requestId"]
    return request_id


# redis扩容缩容
def modify_cache_cluster_step(redis_cap, cluster_id, is_resize):
    res_data = redis_cap.modify_cache_cluster(cluster_id, is_resize)
    request_id = res_data["requestId"]
    return request_id


# Operation-运营删除redis资源
def delete_resource_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_resource(cluster_id)
    request_id = res_data["requestId"]
    return request_id


# Operation-运营删除包年包月未过期redis资源
def delete_no_overdue_resource_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_no_overdue_resource(cluster_id)
    request_id = res_data["requestId"]
    return request_id
