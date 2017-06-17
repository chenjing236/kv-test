# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryFilterCacheClusters :

    @pytest.mark.smoke
    def test_query_filter_cache_clusters(self, config, create_redis_instance, create_redis_month_instance):
        info_logger.info("[Scenario] Test queryFilterCacheClusters")
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        redis_cap_month, cap_month, request_id_for_redis_month, resource_id_month = create_redis_month_instance
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功


        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1

        assert cluster["resource_id"] == resource_id, "[ERROR] QueryFilterCacheClusters use filter feeType=1 is correct!"
        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=601，filterName，验证返回列表包含包年包月实例2

        assert cluster["resource_id"] == resource_id_month, "[ERROR] QueryFilterCacheClusters use filter feeType=601 is correct!"

