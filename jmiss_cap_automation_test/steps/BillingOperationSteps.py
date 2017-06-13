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
    if res_data["code"] is not None:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to pay for the redis [%s], error message is [%s]", order_request_id, error_msg)
        assert False, "[ERROR] It is failed to pay for the redis {0}, error message is {1}".format(order_request_id ,error_msg)
    return request_id
