# -*- coding: utf-8 -*-

# import time
# from business_function.RedisCap import *
from ClusterOperation import *
import logging
info_logger = logging.getLogger(__name__)

# ########################
# 用户操作接口
# ########################


# 循环查询订单状态，返回task执行结果
def query_order_status_step(redis_cap, order_request_id):
    status = 'in_process'
    count = 1
    while status == 'in_process' and count < redis_cap.config["retry_query_order_status_times"]:
        request_id, status = redis_cap.query_order_status(order_request_id)
        info_logger.info("Retry {0} get order status of instance. The status is [{1}]".format(count, status))
        count += 1
        time.sleep(redis_cap.config["wait_time"])
    if count == redis_cap.config["retry_query_order_status_times"] and status == 'inProcess':
        assert False, info_logger.error("Task running time out! The order request_id is {0}".format(order_request_id))
    assert status == 'success', info_logger.error("Redis task execute failed, order request_id is {0}".format(order_request_id))
    # info_logger.info("Task execute end successfully!")
    return


# 循环资源状态，知道资源变为running状态
def query_space_status_step(redis_cap, space_id):
    status = ""
    count = 1
    while status != 'running' and count < redis_cap.config["retry_query_order_status_times"]:
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert error is None
        status = cluster_detail["cacheInstanceStatus"]
        info_logger.info("Retry {0} get space status of instance. The status is [{1}]".format(count, status))
        count += 1
        if status == "error":
            assert False, info_logger.error("Space status is error! space_id is {0}".format(space_id))
        time.sleep(redis_cap.config["wait_time"])
    if count == redis_cap.config["retry_query_order_status_times"] and status != "running":
        assert False, info_logger.error("Task running time out! Now space status is {0}".format(status))
    assert status == "running"
    info_logger.info("Task execute end successfully! Space status become running!")
    return


# 创建缓存云实例，创建接口返回request id
def create_step(redis_cap, create_params, charge_params):
    request_id, result, error = redis_cap.create(create_params, charge_params)
    space_id = ""
    if result is not None:
        space_id = result["cacheInstanceId"]
        info_logger.info("Create request submitted! request_id [{0}], space_id [{1}]".format(request_id, space_id))
        assert error is None
        query_order_status_step(redis_cap, request_id)
        info_logger.info("Create redis cluster successfully! The space_id is [{0}]".format(space_id))
    else:
        info_logger.info("Create request failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return space_id, error


# 创建备份，创建接口返回request_id，base_id
def create_backup_step(redis_cap, instance, space_id, file_name, backup_type=1):
    request_id, result, error = redis_cap.create_backup(space_id, file_name, backup_type)
    base_id = ""
    if result is not None:
        base_id = result["baseId"]
        info_logger.info("Create backup submitted! request_id [{0}], space_id [{1}], base_id [{2}]".format(request_id, space_id, base_id))
        assert error is None
        is_success = get_operation_result_step(instance, space_id, base_id)
        assert is_success is True
        info_logger.info("Create backup successfully!")
    else:
        info_logger.info("Create backup failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return base_id, error


# 查询云缓存实例详情
def query_detail_step(redis_cap, space_id):
    request_id, result, error = redis_cap.query_detail(space_id)
    detail = {}
    if result is not None:
        if space_id == "":
            detail = result["cacheInstances"]
            # info_logger.info("Query redis[{0}] detail successfully! request_id [{1}]".format(space_id, request_id))
        else:
            detail = result["cacheInstance"]
            # info_logger.info("Query redis[{0}] detail successfully! request_id [{1}]".format(space_id, request_id))
    else:
        info_logger.info("Query redis[{0}] detail failed! request_id [{1}], error message [{2}, {3}, {4}]".format(space_id, request_id, error.code, error.status, error.message))
    return detail, error


# 查询资源内部拓扑信息
def query_cluster_info_step(redis_cap, space_id):
    request_id, result, error = redis_cap.query_cluster_info(space_id)
    cluster_info = {}
    if result is not None:
        cluster_info = result["info"]
        info_logger.info("Query redis[{0}] cluster info successfully! request_id [{1}]".format(space_id, request_id))
    else:
        info_logger.info("Query redis[{0}] cluster info failed! request_id [{1}], error message [{2}, {3}, {4}]".format(space_id, request_id, error.code, error.status, error.message))
    return cluster_info, error


# 根据过滤条件查云缓存实例列表
def query_list_step(redis_cap, filter_data=None):
    if filter_data is None:
        filter_data = {}
    cluster_list = []
    total_count = 0
    request_id, result, error = redis_cap.query_list(filter_data)
    if result is not None:
        total_count = result["totalCount"]
        if total_count != 0:
            cluster_list = result["cacheInstances"]
        info_logger.info("Query redis list successfully! request_id is [{0}]".format(request_id))
    else:
        info_logger.info("Query redis list failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return total_count, cluster_list, error


# 根据过滤条件查云缓存备份列表
def query_backup_list_step(redis_cap, space_id, filter_data=None):
    if filter_data is None:
        filter_data = {}
    backup_list = []
    total_count = 0
    request_id, result, error = redis_cap.query_backup_list(space_id, filter_data)
    if result is not None:
        total_count = result["totalCount"]
        if total_count != 0:
            backup_list = result["backups"]
        info_logger.info("Query redis backup list successfully! request_id is [{0}]".format(request_id))
    else:
        info_logger.info("Query redis backup list failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return total_count, backup_list, error


# 根据base_id获取备份文件临时下载链接
def query_download_url_step(redis_cap, space_id, base_id):
    request_id, result, error = redis_cap.query_download_url(space_id, base_id)
    download_urls = []
    if error is None:
        download_urls = result["downloadUrls"]
        info_logger.info("Query redis backup download url successfully! request_id is [{0}]".format(request_id))
    else:
        info_logger.info("Query redis backup download url failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return download_urls, error


# 更新缓存云实例基本信息
def update_meta_step(redis_cap, space_id, name=None, description=None):
    request_id, error = redis_cap.update_meta(space_id, name, description)
    if error is None:
        info_logger.info("Update redis name/description successfully! request_id [{0}]".format(request_id))
    else:
        info_logger.info("Update redis name/description failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return error


# 重置缓存云实例密码
def reset_password_step(redis_cap, space_id, password):
    request_id, error = redis_cap.reset_password(space_id, password)
    if error is None:
        info_logger.info("Reset password to \"{0}\" successfully! request_id [{1}]".format(password, request_id))
    else:
        info_logger.info("Reset password failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return error


# 修改自定义参数
def modify_config_step(redis_cap, space_id, redis_config):
    request_id, error = redis_cap.modify_config(space_id, redis_config)
    if error is None:
        info_logger.info("Modify config successfully! request_id [{0}]".format(request_id))
    else:
        info_logger.info("Modify config failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return error


# 查询自定义参数列表
def query_config_step(redis_cap, space_id):
    request_id, result, error = redis_cap.query_config(space_id)
    config_list = []
    if error is None:
        config_list = result["instanceConfig"]
        info_logger.info("Query config list successfully! request_id [{1}]".format(space_id, request_id))
    else:
        info_logger.info("Query config list failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return config_list, error


# 修改资源自动备份策略
def modify_backup_policy_step(redis_cap, space_id, backupTime, backupPeriod):
    request_id, error = redis_cap.modify_backup_policy(space_id, backupTime, backupPeriod)
    if error is None:
        info_logger.info("Modify backup policy successfully! request_id is [{0}]".format(request_id))
    else:
        info_logger.info("Modify backup policy failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return error


# 查询备份策略
def query_backup_policy_step(redis_cap, space_id):
    request_id, result, error = redis_cap.query_backup_policy(space_id)
    backup_policy = {}
    if error is None:
        backup_policy = result
        info_logger.info("Query backup policy successfully! request_id [{1}]".format(space_id, request_id))
    else:
        info_logger.info("Query backup policy failed! request_id [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return backup_policy, error


# 删除redis实例
def delete_step(redis_cap, space_id, op_delete=0):
    request_id, error = redis_cap.delete(space_id, op_delete)
    if error is None:
        info_logger.info("Delete redis[{0}] successfully! request_id is {1}".format(space_id, request_id))
    else:
        info_logger.info("Delete redis[{0}] failed! request_id is {1}, error message [{2}, {3}, {4}]".format(space_id, request_id, error.code, error.status, error.message))
    return error


# redis扩容缩容
def resize_step(redis_cap, space_id, instance_class):
    request_id, error = redis_cap.resize(space_id, instance_class)
    if error is None:
        info_logger.info("Resize request submitted! space_id [{0}], request_id [{1}]".format(space_id, request_id))
        query_order_status_step(redis_cap, request_id)
        info_logger.info("Resize redis cluster successfully!")
    else:
        info_logger.info("Resize request failed! space_id [{0}], request_id [{1}], error message [{2}, {3}, {4}]".format(space_id, request_id, error.code, error.status, error.message))
    return error


# redis根据备份文件进行恢复
def restore_step(redis_cap, space_id, base_id):
    request_id, error = redis_cap.restore(space_id, base_id)
    if error is None:
        info_logger.info("Restore request submitted! space_id [{0}], request_id [{1}]".format(space_id, request_id))
        query_space_status_step(redis_cap, space_id)
        info_logger.info("Restore redis successfully!")
    else:
        info_logger.info("Restore request failed! space_id [{0}], request_id [{1}], error message [{2}, {3}, {4}]".format(space_id, request_id, error.code, error.status, error.message))
    return error


# 查询flavor列表
def query_flavor_step(redis_cap):
    request_id, result, error = redis_cap.query_flavor()
    flavor_list = []
    if error is None:
        flavor_list = result["instanceClasses"]
        info_logger.info("Query instance class successfully! request_id is [{0}]".format(request_id))
    else:
        info_logger.info("Query instance class failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return flavor_list, error


# 查询当前配额使用情况
def query_quota_step(redis_cap):
    request_id, result, error = redis_cap.query_quota()
    quota = 0
    used = 0
    if error is None:
        quota = result["quota"]["max"]
        used = result["quota"]["used"]
        info_logger.info("Query user quota successfully! request_id is [{0}], quota = {1}, used = {2}".format(request_id, quota, used))
    else:
        info_logger.info("Query user quota failed! request_id is [{0}], error message [{1}, {2}, {3}]".format(request_id, error.code, error.status, error.message))
    return quota, used, error


# #####################
# 运营后台操作接口
# #####################


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
