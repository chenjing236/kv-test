# -*- coding: utf-8 -*-

import json
import logging
import time

from business_function.MongoCap import *

logger_info = logging.getLogger(__name__)

#创建缓存云实例，创建接口返回request id
def create_mongo_instance_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.create_instance()
    request_id = res_data["requestId"]
    if res_data["code"] is not None:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id

