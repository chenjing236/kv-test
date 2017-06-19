# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryResizeCachePrice:

    @pytest.mark.smoke
    def test_query_resize_cache_price(self, create_redis_instance, config, instance_data, redis_http_client):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        print cluster
        memory = cluster["capacity"]+1
        print cluster["spaceId"]
        info_logger.info("[Scenario] Test queryResizeCachePrice")
        request_id, price = query_resize_cache_price_step(redis_cap, "redis-xref3i1mbb", memory)
        info_logger.info("[Scenario] queryResizeCachePrice result:{0},{1}".format(request_id, price))
        info_logger.info("[INFO] Test QueryResizeCachePrice  successfully!")


