# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.BillingOperationSteps import query_order_status_step
from steps.RedisClusterOperationSteps import create_redis_month_instance_with_new_payment_step, \
    create_redis_instance_step

logger_info = logging.getLogger(__name__)

# 创建redis实例
def create_an_instance_with_new_payment(redis_cap,cap):
    # 创建redis实例
    info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
    request_id_for_redis = create_redis_instance_step(redis_cap)
    # 查询订单状态
    info_logger.info("[STEP] Query order status, check the status of order")
    success, resource_id = query_order_status_step(cap, request_id_for_redis)
    return resource_id
