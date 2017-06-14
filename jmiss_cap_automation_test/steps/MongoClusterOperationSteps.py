# -*- coding: utf-8 -*-

import json
import logging
import time

from business_function.MongoCap import *

logger_info = logging.getLogger(__name__)

#创建mongo实例，创建接口返回request id
def create_mongo_instance_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.create_instance()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id

#查询monggo详情
def query_mongo_db_detail_step(config, instance_data, http_client, resource_id):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_mongo_db_detail(resource_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    mongo_detail = res_data["mongodbDetail"]
    return request_id, mongo_detail

#删除mongo实例，删除接口返回request_id
def delete_mongo_instance_step(config, instance_data, http_client, resource_id):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.delete_mongo_db(resource_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id
