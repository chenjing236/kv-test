# -*- coding: utf-8 -*- 
import sys
import json
import time
from business_function.Cap import *
reload(sys)
sys.setdefaultencoding('utf-8')

logger_info = logging.getLogger(__name__)


# 查询订单状态
def query_order_status_step(cap, order_request_id):
    res_data = cap.query_order_status(order_request_id)
    success = res_data["success"]
    inProcess = res_data["inProcess"]
    total = res_data["total"]
    assert success + inProcess == 1 and total == 1, "[ERROR] Query order status response is wrong!"
    count = 1
    while inProcess == 1 and count < cap.config["retry_getting_info_times"]:
        res_data = cap.query_order_status(order_request_id)
        inProcess = res_data["inProcess"]
        logger_info.info("[INFO] Retry {0} get order status of instance. {1}".format(count, json.dumps(res_data)))
        count += 1
        time.sleep(cap.config["wait_time"])
    success = res_data["success"]
    assert inProcess == 0 and success == 1, "[ERROR] Create redis instance failed!"
    resourceId = res_data["resourceIds"][0]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query redis order status [%s], error message is [%s]", order_request_id, error_msg)
        assert False, "[ERROR] It is failed to query redis order status {0}, error message is {1}".format(order_request_id, error_msg)
    return success, resourceId


# 查询订单详情
def query_order_detail_step(cap, order_request_id):
    res_data = cap.query_order_detail(order_request_id)
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query redis order detail [%s], error message is [%s]", order_request_id, error_msg)
        assert False, "[ERROR] It is failed to query redis order detail {0}, error message is {1}".format(order_request_id, error_msg)
    feeType = res_data["feeType"]
    return feeType


# 查询用户配额
def query_user_quota_step(cap, resource):
    res_data = cap.query_user_quota(resource)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to query user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to query user quota, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["use"]


# Operation-运营删除redis资源
def delete_resource_step(cap, cluster_id):
    res_data = cap.delete_resource(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to delete resource by operation [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to delete resource by operation {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id


# Operation-运营删除包年包月未过期redis资源
def delete_no_overdue_resource_step(cap, cluster_id):
    res_data = cap.delete_no_overdue_resource(cluster_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to delete no_overdue resource by operation [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        assert False, "[ERROR] It is failed to delete no_overdue resource by operation {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id


# Operation-运营停服redis资源
def stop_resource_step(cap, cluster_id):
    res_data = cap.stop_resource(cluster_id)
    request_id = res_data["requestId"]
    print res_data
    if "code" in res_data:
        code = res_data["code"]
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to stop resource by operation [%s], resource_id is [%s] error message is [%s]", request_id, cluster_id, error_msg)
        if code == "InternalError" and "置计费状态失败" in error_msg:
            logger_info.info("[INFO] Set bill ae state failed, but the operation stop cache api is not wrong!")
        else:
            assert False, "[ERROR] It is failed to stop resource by operation {0}, resource_id is {1} error message is {2}".format(request_id, cluster_id, error_msg)
    return request_id


# Operation-修改用户可见flavor
def modify_user_visible_flavor_step(cap, cpu, memory, disk, net, max_conn, action_type):
    res_data = cap.modify_user_visible_flavor(cpu, memory, disk, net, max_conn, action_type)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to modify user visible flavor by operation [%s], error message is [%s]", request_id, error_msg)
        assert False, "[ERROR] It is failed to modify user visible flavor by operation {0}, error message is {1}".format(request_id, error_msg)
    return request_id


# Operation-修改用户配额
def modify_used_quota_step(cap, resource, quota):
    res_data = cap.modify_used_quota(resource, quota)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to modify user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to modify user quota, error message is {0}".format(error_msg)
    return request_id, res_data["quota"], res_data["use"]


# Operation-设置用户总配额
def modify_total_quota_step(cap, resource, quota):
    res_data = cap.modify_total_quota(resource, quota)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to set user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to set user quota, error message is {0}".format(error_msg)
    return request_id
