# -*- coding: utf-8 -*-

import json
import logging
import time
from BillingOperationSteps import *

from business_function.MongoCap import *

logger_info = logging.getLogger(__name__)

#创建mongo实例，类型为按配置
def create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client):
    info_logger.info(
        "[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    request_id_for_mongo = create_mongo_instance_with_param_step(config, instance_data, mongo_http_client)
    info_logger.info("[INFO] The mongo instance is created, and the request id is %s", request_id_for_mongo)
    # 支付
    info_logger.info("[STEP] Pay for the mongo instance")
    request_id_for_paying_mongo = pay_for_mongo_instance_step(config, instance_data, cap_http_client,
                                                              request_id_for_mongo)
    info_logger.info("[INFO] The request id is %s for paying mongo", request_id_for_paying_mongo)
    # 查询订单状态
    info_logger.info("[STEP] Get the status of the order for the mongo instance")
    success, resource_id = query_order_status_for_mongo_step(config, instance_data, cap_http_client,
                                                             request_id_for_mongo)
    info_logger.info("[INFO] The resource id is %s for the mongo", resource_id)
    # 查询详情接口
    info_logger.info("[STEP] Get the detail info of the mongo instance")
    request_id, mongo_info = query_mongo_db_detail_step(config, instance_data, mongo_http_client, resource_id)
    print "= ============================ {0}".format(mongo_info)
    if mongo_info is None:
        info_logger.info("[ERROR] The mongo instance %s is not be created", resource_id)
        assert False, "[ERROR] The mongo instance %s is not be created".format(resource_id)
    assert mongo_info["status"] == 100, "[ERROR] The mongo instance %s is not be created".format(resource_id)

    return resource_id, mongo_info

#创建mongo实例，类型为按配置
def create_mongo_instance_with_param_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.create_instance_param(instance_data)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"],ensure_ascii=False).encode("gbk")
        logger_info.error("[ERROR] It is failed to create a mongo instance, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to create a mongo instance, error message is {0}".format(error_msg)
    return request_id

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


def create_mongo_instance_yearly_fee_step(config, instance_data, mongo_http_client, cap_http_client):
    info_logger.info("[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    request_id_for_mongo = create_mongo_instance_with_yealy_fee_step(config, instance_data, mongo_http_client)
    info_logger.info("[INFO] The mongo instance is created, and the request id is %s", json.dumps(request_id_for_mongo))
    # 支付
    info_logger.info("[STEP] Pay for the mongo instance")
    request_id_for_paying_mongo = pay_for_mongo_instance_step(config, instance_data, cap_http_client, request_id_for_mongo)
    info_logger.info("[INFO] The request id is %s for paying mongo", request_id_for_paying_mongo)
    # 查询订单状态
    info_logger.info("[STEP] Get the status of the order for the mongo instance")
    success, resource_id = query_order_status_for_mongo_step(config, instance_data, cap_http_client, request_id_for_mongo)
    info_logger.info("[INFO] The resource id is %s for the mongo", resource_id)
    # 查询详情接口
    info_logger.info("[STEP] Get the detail info of the mongo instance")
    request_id, mongo_info = query_mongo_db_detail_step(config, instance_data, mongo_http_client, resource_id)
    if mongo_info is None:
        info_logger.info("[ERROR] The mongo instance %s is not be created", resource_id)
        assert False, "[ERROR] The mongo instance %s is not be created".format(resource_id)
    assert mongo_info["status"] == 100, "[ERROR] The mongo instance %s is not be created".format(resource_id)
    return resource_id, mongo_info


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

#批量删除mongo实例
def delete_mongo_instances_step(config, instance_data, http_client, resource_ids):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.delete_mongo_dbs(resource_ids)
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

# 查询mongodbs列表
def get_filter_mongo_dbs_step(config, instance_data, http_client,mongo_db_name,page_num):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_filter_mongo_dbs(mongo_db_name,page_num)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get filter mongodbs, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get filter mongodbs, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["mongoDbInfos"]

# 查询mongodbs列表
def get_mongo_dbs_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_mongo_dbs()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get mongodbs, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get mongodbs, error message is {0}".format(error_msg)
    return request_id, res_data["mongoDbs"]

# 查询实时信息
def get_mongo_reailTimeInfo_step(config, instance_data, http_client, resource_ids):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_mongo_realTimeInfo(resource_ids)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get reailTimeInfo, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get reailTimeInfo, error message is {0}".format(error_msg)
    return request_id, res_data["realTimeInfos"]

# 查询拓扑结构
def get_mongo_topology_step(config, instance_data, http_client,resource_id):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_mongo_topology(resource_id)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get topology, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get topology, error message is {0}".format(error_msg)
    return request_id, res_data["primary"], res_data["secondary"], res_data["hidden"]

# 查询vpc列表
def get_vpcs_step(config, instance_data, http_client):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_vpcs()
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get vpcs, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get vpcs, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["vpcs"]

# 查询vpc子网列表
def get_vpc_subnets_step(config, instance_data, http_client, vpcId):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_vpc_subnets(vpcId)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get vpc subnets, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get vpc subnets, error message is {0}".format(error_msg)
    return request_id, res_data["total"], res_data["subNets"]

# 查询vpc详情
def get_vpc_detail_step(config, instance_data, http_client, vpcId):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_vpc_detail(vpcId)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get vpc detail, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get vpc detail, error message is {0}".format(error_msg)
    return request_id, res_data["vpc"]

# 查询vpc子网详情
def get_vpc_subnet_detail_step(config, instance_data, http_client, subnetId):
    mongo_cap = MongoCap(config, instance_data, http_client)
    res_data = mongo_cap.query_vpc_subnet_detail(subnetId)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to get vpc subnet detail, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to get vpc subnet detail, error message is {0}".format(error_msg)
    return request_id, res_data["vpc"]
