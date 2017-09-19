# -*- coding: utf-8 -*- 

# import pytest
# import logging
from BasicTestCase import *
from steps.BillingOperationSteps import *
from steps.RedisClusterOperationSteps import *


class TestResizeRedis:

    @pytest.mark.resize
    def test_resize_an_instance(self, instance_data, create_redis_instance):
        info_logger.info("[Scenario] Start to resize redis cluster")
        # 创建redis实例用于扩容
        info_logger.info("[STEP] Create a redis cluster for resizing")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        info_logger.info("[INFO] Create redis cluster successfully, the resourceId is {0}".format(resource_id))
        # 查询资源capacity
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        capacity = int(cluster["capacity"])
        # 查询升降配尾款账单余额
        #info_logger.info("[STEP] Query redis resize final payment")
        #final_payment_price = query_config_redis_final_payment_step(cap, resource_id)
        #assert final_payment_price == capacity * 3.28, "[ERROR] The final payment price is wrong!"
        #info_logger.info("[INFO] Check redis resize final payment price successfully, the price is {0}".format(final_payment_price))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Resize redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
        # 调用支付接口
        #info_logger.info("[STEP] Pay for resize order")
        #pay_for_redis_instance_step(cap, request_id_resize)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query resize order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Redis resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"
        info_logger.info("[INFO] Test redis cluster resize successfully!")

    @pytest.mark.resize
    def test_reduce_an_instance(self, instance_data, create_redis_instance):
        info_logger.info("[Scenario] Start to reduce redis cluster")
        # 创建redis实例用于扩容
        info_logger.info("[STEP] Create a redis cluster for reducing")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        info_logger.info("[INFO] Create redis cluster successfully, the resourceId is {0}".format(resource_id))
        # 查询资源capacity
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        capacity = int(cluster["capacity"])
        # 查询升降配尾款账单余额
        #info_logger.info("[STEP] Query redis reduce final payment")
        #final_payment_price = query_config_redis_final_payment_step(cap, resource_id)
        #assert final_payment_price == capacity * 3.28, "[ERROR] The final payment price is wrong!"
        #info_logger.info("[INFO] Check redis reduce final payment price successfully, the price is {0}".format(final_payment_price))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Reduce redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 0)
        # 调用支付接口
        #info_logger.info("[STEP] Pay for reduce order")
        #pay_for_redis_instance_step(cap, request_id_resize)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query reduce order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Reduce resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(
            instance_data["create_cache_cluster"]["reduce_capacity"]), "[ERROR] The info of redis reduced is wrong!"
        info_logger.info("[INFO] Test reduce cluster resize successfully!")
