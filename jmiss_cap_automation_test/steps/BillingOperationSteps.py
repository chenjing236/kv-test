# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time
from business_function.Cap import *

logger_info = logging.getLogger(__name__)

# 支付
def pay_for_redis_instance_step(cap, order_request_id):
    request_id_coupon, coupons = query_available_coupons_step(cap.config, cap.instance_data, cap.httpClient, cap.instance_data["redis_coupon_info"])
    if len(coupons) == 0 or coupons[0]["balance"] < 5:
        res_data = cap.pay(order_request_id)
    else:
        coupon_id = coupons[0]["id"]
        res_data = cap.pay(order_request_id, coupon_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to pay for the redis [%s], error message is [%s]", order_request_id, error_msg)
        assert False, "[ERROR] It is failed to pay for the redis {0}, error message is {1}".format(order_request_id, error_msg)
    return request_id


# 订单支付
def pay_for_mongo_instance_step(config, instance_data, http_client, order_request_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.pay(order_request_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to pay for the redis [%s], error message is [%s]", order_request_id, error_msg)
        assert False, "[ERROR] It is failed to pay for the redis {0}, error message is {1}".format(order_request_id, error_msg)
    return request_id


# 查询订单状态
def query_order_status_step(config, instance_data, http_client, order_request_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.query_order_status(order_request_id)
    # request_id = res_data["requestId"]
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

# 查询mongo的订单状态
def query_order_status_for_mongo_step(config, instance_data, cap_http_client, order_request_id):
    cap = Cap(config, instance_data, cap_http_client)
    res_data = cap.query_order_status(order_request_id)
    # request_id = res_data["requestId"]
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
    assert inProcess == 0 and success == 1, "[ERROR] Create mongo instance failed!"
    resourceId = res_data["resourceIds"][0]
    if "code" in res_data:
	error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
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

# 查询订单详情
def recreate_failure_order_step(cap, old_request_id):
    res_data = cap.recreate_failure_order(old_request_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to recreate failure order [%s], error message is [%s]", old_request_id, error_msg)
        assert False, "[ERROR] It is failed to recreate failure order {0}, error message is {1}".format(old_request_id, error_msg)
    return request_id

# 查询redis升降配尾款余额
def query_config_redis_final_payment_step(cap, redis_id):
    res_data = cap.query_config_redis_final_payment(redis_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query redis config final payment [%s], resource_id is [%s], error message is [%s]", request_id, redis_id, error_msg)
        assert False, "[ERROR] It is failed to query config final payment {0}, resource_id is {1}, error message is {2}".format(request_id, redis_id, error_msg)
    price = res_data["price"]
    return price


# 查询redis资源价格
def query_cache_price_step(cap, memory, spaceType, feeType):
    res_data = cap.query_cache_price(memory, spaceType, feeType)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query cache price [%s], error message is [%s]", request_id, error_msg)
        assert False, "[ERROR] It is failed to query cache price {0}, error message is {1}".format(request_id, error_msg)
    price = res_data["price"]
    return price


# 批量查询redis续费价格
def query_renew_prices_step(cap, resource_id, feeType):
    res_data = cap.query_renew_prices(resource_id, feeType)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query renew prices [%s], error message is [%s]", request_id, error_msg)
        assert False, "[ERROR] It is failed to query renew prices {0}, error message is {1}".format(request_id, error_msg)
    price = res_data["total"]
    return price


# 查询redis计费订单
def query_bill_order_step(cap, resource_id):
    res_data = cap.query_bill_order(resource_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query bill order [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to query bill order {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    billing_order = res_data["billingOrder"]
    feeType = billing_order["feeType"]
    return feeType


# 根据resourceId查询资源状态--续费使用
def query_status_by_resource_id_step(cap, resource_id):
    res_data = cap.query_status_by_resource_id(resource_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to query status by resource_id [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to query status by resource_id {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    statusByResourceIdResponseList = res_data["statusByResourceIdResponseList"]
    return statusByResourceIdResponseList


# 批量续费
def renew_billing_orders_step(cap, resource_id, feeType):
    res_data = cap.renew_billing_orders(resource_id, feeType)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to renew billing orders [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to renew billing orders {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id

# 查询mongo的价格
def query_mongo_db_price_step(config, instance_data, httpClient, flavor_info):
    cap = Cap(config, instance_data, httpClient)
    res_data = cap.query_mongo_db_price(flavor_info)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to get the price of the mongo, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get the price of the mongo, error message is {0}".format(error_msg)
    request_id = res_data["requestId"]
    return request_id, res_data

# 查询mongo的折扣信息
def query_min_discount_step(config, instance_data, httpClient, discount_info):
    cap = Cap(config, instance_data, httpClient)
    res_data = cap.query_mongo_db_discount(discount_info)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to get the min discount for the mongo, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get the min discount, error message is {0}".format(error_msg)
    request_id = res_data["requestId"]
    return request_id, res_data

# 查询可用代金券
def query_available_coupons_step(config, instance_data, httpClient, coupon_info):
    cap = Cap(config, instance_data, httpClient)
    res_data = cap.query_available_coupons(coupon_info)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed query available coupon, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to query available coupon, error message is {0}".format(error_msg)
    request_id = res_data["requestId"]
    return request_id, res_data["coupons"]

# 查询用户配额
def query_user_quota_step(config, instance_data, http_client, resource):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.query_user_quota(resource)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to query user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to query user quota, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["use"]

# 修改用户配额
def modify_user_quota_step(config, instance_data, http_client, resource, quota):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.modify_user_quota(resource,quota)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to modify user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to modify user quota, error message is {0}".format(error_msg)
    return request_id, res_data["quota"], res_data["use"]

# 设置用户总配额
def set_user_quota_step(config, instance_data, http_client, resource, quota):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.set_user_quota(resource,quota)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to set user quota, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to set user quota, error message is {0}".format(error_msg)
    return request_id

# 查询计费订单列表
def query_billing_orders_step(config, instance_data, httpClient, condition):
    cap = Cap(config, instance_data, httpClient)
    res_data = cap.query_billing_orders(condition)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed query billing orders, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to query billing orders, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["billingOrders"]
