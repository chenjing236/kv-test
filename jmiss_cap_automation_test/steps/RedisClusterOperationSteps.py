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
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a redis [%s], error message is [%s]", request_id, error_msg)
        assert False, "[ERROR] It is failed to create a redis {0}, error message is {1}".format(request_id, error_msg)
    return request_id


# 创建包年包月缓存云实例，创建接口返回request id
def create_redis_month_instance_step(redis_cap):
    res_data = redis_cap.create_month_instance()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a month redis [%s], error message is [%s]", request_id, error_msg)
        assert False, "[ERROR] It is failed to create a month redis {0}, error message is {1}".format(request_id, error_msg)
    return request_id


# 查询云缓存实例详情
def query_cache_cluster_detail_step(redis_cap, cluster_id):
    res_data = redis_cap.query_cache_cluster_detail(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to query cache cluster detail [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to query cache cluster detail {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    billing_order = res_data["billingOrder"]
    cluster = res_data["cluster"]
    return billing_order, cluster

# 根据过滤条件查云缓存实例列表
def query_filter_cache_clusters_step(redis_cap, filter_data):
    res_data = redis_cap.query_filter_cache_clusters(filter_data)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to query filter cache clusters [%s], filter is [%s] error message is [%s]", request_id, json.dumps(filter_data), error_msg)
        assert False, "[ERROR] It is failed to query filter cache clusters {0}, filter is {1} error message is {2}".format(request_id, json.dumps(filter_data), error_msg)
    clusters = res_data["clusters"]
    return clusters

# 更新缓存云实例基本信息
def update_cache_cluster_step(redis_cap, space_id, update_data):
    res_data = redis_cap.update_cache_cluster(space_id, update_data)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to update cache cluster [%s], resource_id is [%s] error message is [%s]", request_id, space_id, error_msg)
        assert False, "[ERROR] It is failed to update cache cluster {0}, resource_id is {1} error message is {2}".format(request_id, space_id, error_msg)
    return request_id

# 删除redis资源
def delete_redis_instance_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_cache_cluster(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to delete redis instance [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to delete redis instance {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id


# redis扩容缩容
def modify_cache_cluster_step(redis_cap, cluster_id, is_resize):
    res_data = redis_cap.modify_cache_cluster(cluster_id, is_resize)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to resize cache cluster [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to resize cache cluster {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id

# 启动缓存云实例
def start_cache_cluster_step(redis_cap, space_id):
    res_data = redis_cap.start_cache_cluster(space_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to start redis instance [%s], resource_id is [%s] error message is [%s]", request_id, space_id, error_msg)
        assert False, "[ERROR] It is failed to start redis instance {0}, resource_id is {1} error message is {2}".format(request_id, space_id, error_msg)
    return request_id

# 停服缓存云实例
def stop_cache_cluster_step(redis_cap, space_id):
    res_data = redis_cap.stop_cache_cluster(space_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to stop redis instance [%s], resource_id is [%s] error message is [%s]", request_id, space_id, error_msg)
        assert False, "[ERROR] It is failed to stop redis instance {0}, resource_id is {1} error message is {2}".format(request_id, space_id, error_msg)
    return request_id

# Operation-运营删除redis资源
def delete_resource_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_resource(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to delete resource by operation [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to delete resource by operation {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id


# Operation-运营删除包年包月未过期redis资源
def delete_no_overdue_resource_step(redis_cap, cluster_id):
    res_data = redis_cap.delete_no_overdue_resource(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to delete no_overdue resource by operation [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to delete no_overdue resource by operation {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id
