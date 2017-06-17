# -*- coding: utf-8 -*-

import json
import logging
import time

from business_function.MongoCap import *

logger_info = logging.getLogger(__name__)

#创建mongo实例，类型为按配置
def create_mongo_instance_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.create_instance()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"],ensure_ascii=False).encode("gbk")
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id

# 创建mongo实例，类型为包年包月
def create_mongo_instance_with_yealy_fee_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.create_instance_with_yearly_fee()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"],ensure_ascii=False).encode("gbk")
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

#修改mongo实例名称
def modify_mongo_db_name_step(config, instance_data, http_client, resource_id, resource_name):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.modify_mongo_db_name(resource_id, resource_name)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id

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

# 查询flavor列表
def get_flavor_list_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_flavors("mongodb")
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id, res_data["flavors"]

def query_mongo_dbs_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_mongo_dbs("mongodb")
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id, res_data["flavors"]

