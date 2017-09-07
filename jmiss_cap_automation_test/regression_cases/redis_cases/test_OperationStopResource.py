# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestOperationStopResource:

    @pytest.mark.smoke
    def test_stop_resource(self, create_redis_instance):
        #创建云缓存资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))

        #调用运营接口停止资源，接口返回成功（中间层查询不了acl表enable值，无法做正确性验证）
        # 对于未欠费未过期资源计费不支持stop操作，运营stop接口会返回错误，模拟欠费过期操作待完善
        stop_resource_step(redis_cap, resource_id)
        info_logger.info("[INFO] Test operation stop resource successfully!")
