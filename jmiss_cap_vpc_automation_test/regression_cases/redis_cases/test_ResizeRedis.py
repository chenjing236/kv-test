# -*- coding: utf-8 -*- 

# import pytest
# import logging
from BasicTestCase import *
from steps.CapOperationSteps import *
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
        memory = int(cluster["flavorDetail"]["memory"])
        info_logger.info("[INFO] The memory of cluster is {0}".format(memory))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Resize redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query resize order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Redis resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["flavorDetail"]["memory"] == int(
            instance_data["redis_cluster_info"]["flavor_resize"]["memory"]), "[ERROR] The memory of redis resized is wrong!"
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
        memory = int(cluster["flavorDetail"]["memory"])
        info_logger.info("[INFO] The memory of cluster is {0}".format(memory))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Reduce redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 0)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query reduce order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Reduce resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["flavorDetail"]["memory"] == int(
            instance_data["redis_cluster_info"]["flavor_reduce"]["memory"]), "[ERROR] The memory of redis reduced is wrong!"
        info_logger.info("[INFO] Test reduce cluster resize successfully!")
