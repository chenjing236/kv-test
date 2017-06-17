# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryFilterCacheClusters :

    @pytest.mark.smoke
    def test_query_filter_cache_clusters(self, create_redis_instance, create_redis_month_instance):
        info_logger.info("[Scenario] Test queryFilterCacheClusters")
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        redis_cap_month, cap_month, request_id_for_redis_month, resource_id_month = create_redis_month_instance
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功
        filter_data = {}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        for cluster in clusters:
            info_logger.info("[Scenario]queryFilterCacheClusters result with no filter:{0}".format(cluster))


        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1
        filter_data = {"filterStatus":"100","category":"1","filterName":"cap_auto_test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(cluster)))
            assert "cap_auto_test" in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=1 is incorrect!"
            assert cluster["billingOrder"]["category"] == 1, "[ERROR] QueryFilterCacheCluster use filter category=6 is incorrect"

        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=6，filterName，验证返回列表包含包年包月实例2
        filter_data = {"filterStatus":"100","category":"6","filterName":"cap_auto_test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            assert ("cap_auto_test") in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=6 is correct!"
            assert cluster["billingOrder"]["category"] == 6, "[ERROR] QueryFilterCacheCluster use filter category=6 is incorrect"

        info_logger.info("[INFO] Test query filter cacheClusters successfully!")

