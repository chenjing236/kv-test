# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestDeleteCacheClusters:

    @pytest.mark.smoke
    def test_delete_cache_clusters(self, create_redis_instance_no_teardown):
        #创建主从版按配置redis资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance_no_teardown
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #创建集群版按配置redis资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap_2, cap_2, request_id_2, resource_id_2 = create_redis_instance_no_teardown
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #调用批量删除接口
        cluster_ids =[request_id,resource_id_2]
        delete_cache_clusters_step(redis_cap, cluster_ids)

        #验证返回信息正确

        info_logger.info("[INFO] Test delete cacheClusters successfully!")


