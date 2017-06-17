# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryCacheClusterDetailByOrder:

    @pytest.mark.smoke
    def test_query_Cache_cluster_detail_by_order(self, create_redis_instance):
        #创建云缓存资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #根据订单ID查询云缓存实例详情


        assert cluster["resource_id"] == resource_id ,"[ERROR]QueryCacheClusterDetailByOrder return the wrong resource_id"