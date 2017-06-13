# -*- coding: utf-8 -*- 

import pytest
import logging

from steps.ClusterOperationSteps import *
from steps.BillingOperationSteps import *

info_logger = logging.getLogger(__name__)

# 创建redis实例
@pytest.fixture(scope="class")
def create_redis_instance(self, config, data, http_client):
    # 创建redis实例
    info_logger.info("[STEP] Create a Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_mongo_instance_step(config, instance_data, http_client)
    # 支付
    request_id_for_paying_redis = pay_for_redis_instance_step(config, instance_data, http_client, request_id_for_redis)
    # 查询订单状态
    status, clusterId = query_order_status_step(config, instance_data, http_client, request_id_for_paying_redis)
    # 查询详情接口
    cluster, billing_order= query_cache_cluster_detail_step(config, instance_data, http_client, clusterId)
    # tear down 删除redis实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the redis instance %s", clusterId)
        delete_redis_instance_step(config, instance_data, http_client, clusterId)

    request.addfinalizer(teardown)
    return request_id
