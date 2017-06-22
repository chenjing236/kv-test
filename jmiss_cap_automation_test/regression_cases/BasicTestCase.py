# -*- coding: utf-8 -*- 

import pytest
import logging

from steps.OperationSteps import *
from steps.RedisClusterOperationSteps import *
from steps.MongoClusterOperationSteps import *
from steps.BillingOperationSteps import *

info_logger = logging.getLogger(__name__)

# 创建按配置计费redis实例
@pytest.fixture(scope="session")
def create_redis_instance(config, instance_data, redis_http_client, cap_http_client, request):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(redis_cap)
    # 支付
    info_logger.info("[STEP] Pay for the create order of redis instance")
    pay_for_redis_instance_step(cap, request_id_for_redis)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resource_id = query_order_status_step(cap, request_id_for_redis)
    # 查询详情接口
    info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
    billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"

    # tear down 删除redis实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
        delete_redis_instance_step(redis_cap, resource_id)

    request.addfinalizer(teardown)
    return redis_cap, cap, request_id_for_redis, resource_id

# 创建按配置计费redis实例
@pytest.fixture(scope="session")
def create_redis_instance_no_teardown(config, instance_data, redis_http_client, cap_http_client, request):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(redis_cap)
    # 支付
    info_logger.info("[STEP] Pay for the create order of redis instance")
    pay_for_redis_instance_step(cap, request_id_for_redis)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resource_id = query_order_status_step(cap, request_id_for_redis)
    # 查询详情接口
    info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
    billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"

    # # tear down 删除redis实例
    # def teardown():
    #     info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
    #     delete_redis_instance_step(redis_cap, resource_id)
    #
    # request.addfinalizer(teardown)
    return redis_cap, cap, request_id_for_redis, resource_id


# 创建包年包月redis实例
@pytest.fixture(scope="session")
def create_redis_month_instance(config, instance_data, redis_http_client, cap_http_client, request):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_month_instance_step(redis_cap)
    # 支付
    info_logger.info("[STEP] Pay for the create order of redis instance")
    request_id_for_paying_redis = pay_for_redis_instance_step(cap, request_id_for_redis)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resource_id = query_order_status_step(cap, request_id_for_redis)
    # 查询详情接口
    info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
    billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"

    # tear down 删除redis实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
        delete_no_overdue_resource_step(redis_cap, resource_id)

    request.addfinalizer(teardown)
    return redis_cap, cap, request_id_for_redis, resource_id

# 创建mongo实例,类型为按配置
@pytest.fixture(scope="session")
def create_mongo_instance(request, config, instance_data, mongo_http_client, cap_http_client):
    info_logger.info("[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    request_id_for_mongo = create_mongo_instance_step(config, instance_data, mongo_http_client)
    info_logger.info("[INFO] The mongo instance is created, and the request id is %s", request_id_for_mongo)
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

    # 删除mongo实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", resource_id)
        request_id_for_delete_mongo = delete_mongo_instance_step(config, instance_data, mongo_http_client, resource_id)

    request.addfinalizer(teardown)
    return resource_id, mongo_info

# 创建mongo实例,类型为包年包月
@pytest.fixture(scope="class")
def create_mongo_instance_with_yearly_fee(request, config, instance_data, mongo_http_client, cap_http_client):
    info_logger.info("[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    request_id_for_mongo = create_mongo_instance_with_yearly_fee_step(config, instance_data, mongo_http_client)
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
    request_id_for_mongo = create_mongo_instance_step(config, data_for_instance, mongo_http_client)
    info_logger.info("[INFO] The mongo instance is created, and the request id is %s", request_id_for_mongo)
    # 支付
    info_logger.info("[STEP] Pay for the mongo instance")
    request_id_for_paying_mongo = pay_for_mongo_instance_step(config, data_for_instance, cap_http_client, request_id_for_mongo)
    info_logger.info("[INFO] The request id is %s for paying mongo", request_id_for_paying_mongo)
    # 查询订单状态
    info_logger.info("[STEP] Get the status of the order for the mongo instance")
    success, resource_id = query_order_status_step(config, data_for_instance, cap_http_client, request_id_for_mongo)
    info_logger.info("[INFO] The resource id is %s for the mongo", resource_id)
    # 查询详情接口
    info_logger.info("[STEP] Get the detail info of the mongo instance")
    request_id, mongo_info = query_mongo_db_detail_step(config, data_for_instance, mongo_http_client, resource_id)

    # 删除mongo实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", resource_id)
        request_id_for_delete_mongo = delete_no_overdue_resource_step(config, instance_data, cap_http_client, resource_id)

    request.addfinalizer(teardown)
    return resource_id, mongo_info


# 创建mongo实例,类型为按配置
@pytest.fixture(scope="session")
def create_mongo_instance_three(request, config, instance_data, mongo_http_client, cap_http_client):
    info_logger.info("[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    resource_id, mongo_info = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)

    resource_id2, mongo_info2 = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)
    resource_id3, mongo_info3 = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)

    # 删除mongo实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", resource_id)
        request_id_for_delete_mongo = delete_mongo_instance_step(config, instance_data, mongo_http_client, resource_id)
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", resource_id2)
        request_id_for_delete_mongo = delete_mongo_instance_step(config, instance_data, mongo_http_client, resource_id2)
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", resource_id3)
        request_id_for_delete_mongo = delete_mongo_instance_step(config, instance_data, mongo_http_client, resource_id3)

    request.addfinalizer(teardown)
    return resource_id, mongo_info,resource_id2, mongo_info2,resource_id3, mongo_info3
