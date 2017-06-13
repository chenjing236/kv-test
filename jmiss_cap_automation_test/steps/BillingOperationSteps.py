# -*- coding: utf-8 -*- 

import json
import logging
import time
from business_function.Cap import *

logger_info = logging.getLogger(__name__)

#支付
def pay_for_redis_instance_step(config, instance_data, http_client, order_request_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.pay(order_request_id)
    request_id = res_data["requestId"]
    # if res_data["code"] is not None:
    #     error_msg = res_data["message"]
    #     logger_info.error("[ERROR] It is failed to pay for the redis [%s], error message is [%s]", order_request_id, error_msg)
    #     assert False, "[ERROR] It is failed to pay for the redis {0}, error message is {1}".format(order_request_id, error_msg)
    return request_id

def query_order_status_step(config, instance_data, http_client, order_request_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.query_order_status(order_request_id)
    request_id = res_data["requestId"]
    inProcess = res_data["inProcess"]
    total = res_data["total"]
    assert inProcess == 1 and total == 1, "[ERROR] Query order status response is wrong!"
    count = 1
    while inProcess == 1 and count < config["retry_getting_info_times"]:
        res_data = cap.query_order_status(order_request_id)
        inProcess = res_data["inProcess"]
        logger_info.info("[INFO] Retry {0} get order status of instance. {1}".format(count, res_data))
        count += 1
        time.sleep(config["wait_time"])
    success = res_data["success"]
    assert inProcess == 0 and success == 1, "[ERROR] Create redis instance failed!"
    resourceId = res_data["resourceIds"][0]
    # if res_data["code"] is not None:
    #     error_msg = res_data["message"]
    #     logger_info.error("[ERROR] It is failed to query redis order status [%s], error message is [%s]", order_request_id,
    #                       error_msg)
    #     assert False, "[ERROR] It is failed to query redis order status {0}, error message is {1}".format(order_request_id,
    #                                                                                                error_msg)
    return success, resourceId
