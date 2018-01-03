# -*- coding: utf-8 -*- 


from BasicTestCase import *


class TestSmokeCasesForRedisCap:
    @pytest.mark.smoke
    def test_create_an_instance(self, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))

    @pytest.mark.smoke
    def test_query_filter_cache_clusters(self, create_redis_instance, create_redis_month_instance):
        info_logger.info("[Scenario] Test queryFilterCacheClusters")
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        create_redis_month_instance
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功
        filter_data = {}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        for cluster in clusters:
            info_logger.info("[Scenario]queryFilterCacheClusters result with no filter:{0}".format(cluster))

        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1
        filter_data = {"filterStatus": "100", "category": "1", "filterName": "test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            # info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(cluster)))
            assert "test" in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=1 is incorrect!"
            assert cluster["billingOrder"]["chargeMode"] == 1, "[ERROR] QueryFilterCacheCluster use filter category=1 is incorrect"

        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=6，filterName，验证返回列表包含包年包月实例2
        filter_data = {"filterStatus": "100", "category": "3", "filterName": "test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            assert "test" in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=6 is correct!"
            assert cluster["billingOrder"]["chargeMode"] == 3, "[ERROR] QueryFilterCacheCluster use filter category=3 is incorrect"
        info_logger.info("[INFO] Test query filter cacheClusters successfully!")

    @pytest.mark.smoke
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
            instance_data["redis_cluster_info"]["flavor_resize"][
                "memory"]), "[ERROR] The memory of redis resized is wrong!"
        info_logger.info("[INFO] Test redis cluster resize successfully!")

    @pytest.mark.smoke
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
            instance_data["redis_cluster_info"]["flavor_reduce"][
                "memory"]), "[ERROR] The memory of redis reduced is wrong!"
        info_logger.info("[INFO] Test reduce cluster resize successfully!")
