# -*- coding: utf-8 -*-

import time
from business_function.RedisCap import *

# ########################
# 用户操作接口
# ########################


# 循环查询订单状态，返回task执行结果
def query_order_status_step(redis_cap, order_request_id):
    status = 'in_process'
    count = 1
    while status == 'in_process' and count < redis_cap.config["retry_times"]:
        request_id, status = redis_cap.query_order_status(order_request_id)
        info_logger.info("Retry {0} get order status of instance. The status is [{1}]".format(count, status))
        count += 1
        time.sleep(redis_cap.config["wait_time"])
    if count == redis_cap.config["retry_times"] and status == 'inProcess':
        assert False, info_logger.error("Task running time out! The order request_id is {0}".format(order_request_id))
    assert status == 'success', info_logger.error("Create redis instance failed, order request_id is {0}".format(order_request_id))
    info_logger.info("Task execute end successfully!")
    return


# 创建缓存云实例，创建接口返回request id
def create_step(redis_cap, month=None):
    request_id, space_id = redis_cap.create(month)
    info_logger.info("Create request submitted! space_id [{0}], request_id [{1}]".format(space_id, request_id))
    query_order_status_step(redis_cap, request_id)
    info_logger.info("Create redis cluster successfully! The space_id is [{0}]".format(space_id))
    return space_id


# 查询云缓存实例详情
def query_detail_step(redis_cap, space_id):
    request_id, detail = redis_cap.query_detail(space_id)
    info_logger.info("Query redis[{0}] detail successfully! request_id [{1}]".format(space_id, request_id))
    return detail


# 根据过滤条件查云缓存实例列表
def query_list_step(redis_cap, filter_data=None):
    if filter_data is None:
        filter_data = {}
    request_id, redis_list = redis_cap.query_list(filter_data)
    info_logger.info("Query redis list successfully! request_id is [{0}]".format(request_id))
    return redis_list


# 更新缓存云实例基本信息
def update_meta_step(redis_cap, space_id, name=None, description=None):
    request_id = redis_cap.update_meta(space_id, name, description)
    info_logger.info("Update redis name/description successfully! request_id is [{0}]".format(request_id))
    return


# 删除redis实例
def delete_step(redis_cap, space_id):
    request_id = redis_cap.delete(space_id)
    info_logger.info("Delete redis[{0}] successfully! request_id is {1}".format(space_id, request_id))
    return


# redis扩容缩容
def resize_step(redis_cap, space_id, instance_class):
    request_id = redis_cap.resize(space_id, instance_class)
    info_logger.info("Resize request submitted! space_id [{0}], request_id is [{1}]".format(space_id, request_id))
    query_order_status_step(redis_cap, request_id)
    info_logger.info("Resize redis cluster successfully! The space_id is [{0}]".format(space_id))
    return


# 查询flavor列表
def query_flavor_step(redis_cap):
    request_id, flavor_list = redis_cap.query_flavor()
    info_logger.info("Query instance class successfully! request_id is [{0}]".format(request_id))
    return flavor_list


# 查询当前配额使用情况
def query_quota_step(redis_cap):
    request_id, quota, used = redis_cap.query_quota()
    info_logger.info("Query user quota successfully! request_id is [{0}], quota = {1}, used = {2}".format(request_id, quota, used))
    return quota, used


# #####################
# 运营后台操作接口
# #####################


# Operation-运营删除redis资源
def operation_delete_step(redis_operation, space_id):
    request_id = redis_operation.delete(space_id)
    info_logger.info("Operation delete redis[{0}] successfully! request_id is {1}".format(space_id, request_id))
    return


# Operation-修改用户可见flavor
# 参数为规格代码instance_class，操作类型action_type：1可见，0无效，-1不可见
def modify_user_class_step(redis_operation, instance_class, action_type):
    request_id = redis_operation.modify_user_class(instance_class, action_type)
    info_logger.info("Modify user instance_class[{0}] to {1} successfully! request_id is {2}".format(instance_class, action_type, request_id))
    return


# Operation-修改用户配额
def modify_quota_step(redis_operation, used, quota):
    request_id = redis_operation.modify_quota(used, quota)
    info_logger.info("Modify user quota [used={0}, quota={1}] successfully! request_id is {2}".format(used, quota, request_id))
    return
