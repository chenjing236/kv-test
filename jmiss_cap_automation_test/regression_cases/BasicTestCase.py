# -*- coding: utf-8 -*- 

import pytest
import logging

from steps.RedisClusterOperationSteps import *
from steps.MongoClusterOperationSteps import *
from steps.BillingOperationSteps import *

info_logger = logging.getLogger(__name__)


# 创建redis实例
@pytest.fixture(scope="class")
def create_redis_instance(config, data_for_instance, http_redis_client, http_cap_client, request):
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(config, data_for_instance, http_redis_client)
    # 支付
    info_logger.info("[STEP] Pay for the create order of redis instance")
    request_id_for_paying_redis = pay_for_redis_instance_step(config, data_for_instance, http_cap_client, request_id_for_redis)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resourceId = query_order_status_step(config, data_for_instance, http_cap_client, request_id_for_redis)
    # 查询详情接口
    info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
    billing_order, cluster = query_cache_cluster_detail_step(config, data_for_instance, http_redis_client, resourceId)
    assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"

    # tear down 删除redis实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the redis instance %s", resourceId)
        request_id_for_delete_redis = delete_redis_instance_step(config, data_for_instance, http_redis_client, resourceId)

    request.addfinalizer(teardown)
    return request_id_for_redis, resourceId

# 创建mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance(request, config, data_for_instance, mongo_http_client, cap_http_client):
    info_logger.info("[STEP] Create a mongo instance, the instance consists of primary container, secondary container and hidden container")
    # 创建mongo实例
    request_id_for_mongo = create_mongo_instance_step(config, data_for_instance, mongo_http_client)
    info_logger.info("[INFO] The mongo instance %s is created", request_id)
    # 支付
    info_logger.info("[STEP] Pay for the mongo instance")
    request_id_for_paying_redis = pay_for_mongo_instance_step(config, data_for_instance, cap_http_client, request_id_for_mongo)
    # 查询订单状态
    # 删除mongo实例
    return request_id
