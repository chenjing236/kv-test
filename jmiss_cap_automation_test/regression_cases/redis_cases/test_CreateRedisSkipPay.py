# -*- coding: utf-8 -*-

from BasicTestCase import *


class TestCreateRedisSkipPay:

    @pytest.mark.smoke
    def test_create_an_instance_skip_pay(self, create_redis_instance_skip_pay):
        info_logger.info("[Scenario] Create an instance skipping pay for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance_skip_pay
        info_logger.info("[INFO] Test create redis instance skipping pay successfully, the resourceId is {0}".format(resource_id))