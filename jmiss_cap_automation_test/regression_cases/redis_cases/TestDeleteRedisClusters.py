# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestDeleteCacheClusters:

    @pytest.mark.smoke
    def test_delete_cache_clusters(self, create_redis_instance):
        #创建主从版按配置redis资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #创建集群版按配置redis资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #调用批量删除接口

        #验证返回信息正确

