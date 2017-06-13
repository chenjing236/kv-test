# -*- coding: utf-8 -*- 

import pytest
import logging

#from steps.RedisClusterOperationSteps import *
from steps.MongoClusterOperationSteps import *
#from steps.BillingOperationSteps import *

info_logger = logging.getLogger(__name__)

# 创建redis实例
@pytest.fixture(scope="class")
#def create_redis_instance(self, config, data, redis_http_client):
#    # 创建redis实例
#    info_logger.info("[STEP] Create a Create an instance for redis, the instance consists of a master and a slave")
#    request_id_for_redis = create_mongo_instance_step(config, instance_data, redis_http_client)
#    # 支付
#    request_id_for_paying_redis = pay_for_redis_instance_step(config, instance_data, redis_http_client, request_id_for_redis)
#    # 查询订单状态
#    status, clusterId = query_order_status_step(config, instance_data, redis_http_client, request_id_for_paying_redis)
#    # 查询详情接口
#    cluster, billing_order= query_cache_cluster_detail_step(config, instance_data, redis_http_client, clusterId)
#    # tear down 删除redis实例
#    def teardown():
#        info_logger.info("[TEARDOWN] Delete the redis instance %s", clusterId)
#        delete_redis_instance_step(config, instance_data, redis_http_client, clusterId)
#
#    request.addfinalizer(teardown)
#    return request_id

# 创建mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance(self, config, data, mongo_http_client):
    info_logger.info("[SET UP] Create a mongo instance")
    # 创建mongo实例
    request_id = create_mongo_instance_step(config, data, mongo_http_client)
    info_logger.info("[INFO] The mongo instance %s is created", request_id)
    # 支付
    # 查询订单状态
    # 删除mongo实例
    return request_id
