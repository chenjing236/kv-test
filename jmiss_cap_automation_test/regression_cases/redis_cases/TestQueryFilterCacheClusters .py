# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryFilterCacheClusters :

    @pytest.mark.smoke
    def test_query_filter_cache_clusters(self, config, instance_data, redis_http_client ,cap_http_client):
        info_logger.info("[Scenario] Test queryFilterCacheClusters")
        # 创建按配置计费redis资源，用于列表查询
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        # 创建redis实例
        info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # 支付
        info_logger.info("[STEP] Pay for the create order of redis instance")
        pay_for_redis_instance_step(cap, request_id_for_redis)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create redis instance successfully, the resourceId is {0}".format(resource_id))

        return
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功
        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1
        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=601，filterName，验证返回列表包含包年包月实例2
