# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.BillingOperationSteps import query_order_status_step
from steps.RedisClusterOperationSteps import create_redis_month_instance_with_new_payment_step, \
    create_redis_instance_step
import pytest
logger_info = logging.getLogger(__name__)

# 创建redis实例
@pytest.fixture(scope="session")
def create_an_instance_with_NP(config,instance_data,redis_http_client,cap_http_client):
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(redis_cap)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resource_id = query_order_status_step(cap, request_id_for_redis)
    '''
    #tear down 删除redis实例
    def teardown():
        info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
        delete_redis_instance_step(redis_cap, resource_id)
    request.addfinalizer(teardown)
    '''
    return redis_cap, cap, resource_id

