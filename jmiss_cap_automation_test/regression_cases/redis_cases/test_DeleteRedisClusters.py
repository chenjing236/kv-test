# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestDeleteCacheClusters:

    @pytest.mark.smoke
    def test_delete_cache_clusters(self, config, instance_data, redis_http_client, cap_http_client):
        info_logger.info("[INFO] Test Delete clusters!")
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        # 创建第一个redis实例
        info_logger.info("[STEP] Create the first redis instance")
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # 支付
        #info_logger.info("[STEP] Pay for the create order of redis instance")
        #pay_for_redis_instance_step(cap, request_id_for_redis)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create the first redis instance successfully, the resourceId is {0}".format(resource_id))
        # 创建第二个redis资源
        info_logger.info("[Scenario] Create the second redis instance")
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # 支付
        #info_logger.info("[STEP] Pay for the create order of redis instance")
        #pay_for_redis_instance_step(cap, request_id_for_redis)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id_2 = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create the second redis instance successfully, the resourceId is {0}".format(resource_id))
        # 调用批量删除接口
        info_logger.info("[STEP] Delete the two clusters now")
        cluster_ids = [resource_id, resource_id_2]
        delete_cache_clusters_step(redis_cap, cluster_ids)
        # 验证返回信息正确
        info_logger.info("[INFO] Test delete cacheClusters successfully!")

