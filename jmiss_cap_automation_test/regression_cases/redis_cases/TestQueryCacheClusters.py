# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryCacheClusters:

    @pytest.mark.smoke
    def test_query_cache_clusters(self, create_redis_instance):
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功
        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1
        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=601，filterName，验证返回列表包含包年包月实例2
