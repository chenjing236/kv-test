# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestOperationFlavors:

    @pytest.mark.smoke
    def test_operation_flavors(self, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))


        info_logger.info("[INFO] Test operation flavors successfully!")
