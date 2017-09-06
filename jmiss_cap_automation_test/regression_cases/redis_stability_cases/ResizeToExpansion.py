# -*- coding: utf-8 -*-
import time
from BasicTestCase import *
from steps.BillingOperationSteps import query_order_status_step, pay_for_redis_instance_step
from steps.RedisClusterOperationSteps import modify_cache_cluster_step, query_cache_cluster_detail_step

logger_info = logging.getLogger(__name__)

#扩容
def resize_to_expansion(redis_cap, cap, instance_data, resource_id):
    time.sleep(60)  # 等待一分钟，避免计费超时
    request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
    # 查询订单状态，验证扩容成功
    info_logger.info("[STEP] Query resize order status until resize over")
    success, resource_id = query_order_status_step(cap, request_id_resize)
    assert success == 1, "[ERROR] Redis resize failed!"
    billing_order,cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"