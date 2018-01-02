# -*- coding: utf-8 -*- 

import pytest
from steps.RedisClusterOperationSteps import *
from steps.CapOperationSteps import *

info_logger = logging.getLogger(__name__)


# 创建按配置计费redis实例
@pytest.fixture(scope="class")
def create_redis_instance(config, instance_data, redis_http_client, cap_http_client, request):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(redis_cap)

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


# 创建包年包月redis实例
@pytest.fixture(scope="class")
def create_redis_month_instance(config, instance_data, redis_http_client, cap_http_client, request):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_month_instance_step(redis_cap)

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
        delete_no_overdue_resource_step(cap, resource_id)

    request.addfinalizer(teardown)
    return redis_cap, cap, request_id_for_redis, resource_id
