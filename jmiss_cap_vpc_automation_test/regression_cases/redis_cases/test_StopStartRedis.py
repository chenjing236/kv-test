# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestSetAclForRedis:

    @pytest.mark.smoke
    def test_stop_start_redis(self, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        # 调用中间层停服缓存云实例接口（stopCacheCluster），对云缓存进行停服操作，接口返回成功（中间层查询不了acl表enable值，无法做正确性验证）
        stop_cache_cluster_step(redis_cap, resource_id)
        # 查询详情，结果正确
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        time.sleep(5)
        # 调用中间层启动缓存云实例接口（startCacheCluster），对云缓存进行启动操作，接口返回成功（中间层查询不了acl表enable值，无法做正确性验证）
        start_cache_cluster_step(redis_cap, resource_id)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"

        info_logger.info("[INFO] Test set acl for redis successfully!")


