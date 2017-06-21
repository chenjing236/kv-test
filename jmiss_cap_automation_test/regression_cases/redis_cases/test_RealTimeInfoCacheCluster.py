# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestRealTimeInfoCacheCluster:

    @pytest.mark.smoke
    def test_real_time_info_cache_cluster(self, create_redis_instance):
        #创建云缓存资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #查询实时使用内存
        space_ids = resource_id
        request_id, infos = real_time_info_cache_cluster_step(redis_cap, space_ids)
        if infos is None:
            time.sleep(30)
            request_id, infos = real_time_info_cache_cluster_step(redis_cap, space_ids)

        info_logger.info("[INFO] Test  get realtime info cachecluster successfully!")



