# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestSetAclForRedis:

    @pytest.mark.smoke
    def test_create_an_instance(self, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #调用中间层创建acl规则接口（aclCacheCluster），为创建的云缓存实例添加acl，接口返回成功

        #调用中间层的查询acl规则接口（queryCacheClusterAcl），查询刚添加的acl，调用接口成功，正确返回刚添加的acl

        #调用中间层停服缓存云实例接口（stopCacheCluster），对云缓存进行停服操作，接口返回成功（中间层查询不了acl表enable值，无法做正确性验证）

        #调用中间层启动缓存云实例接口（startCacheCluster），对云缓存进行启动操作，接口返回成功（中间层查询不了acl表enable值，无法做正确性验证）


