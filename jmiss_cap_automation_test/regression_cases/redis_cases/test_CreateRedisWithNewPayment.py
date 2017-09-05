# -*- coding: utf-8 -*-

from BasicTestCase import *


class TestCreateRedisWithNewPayment:

    @pytest.mark.smoke
    def test_create_an_instance_with_new_payment(self, create_redis_month_instance_with_new_payment):
        info_logger.info("[Scenario] Create an instance skipping paying for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_month_instance_with_new_payment
        info_logger.info("[INFO] Test create redis instance skipping paying successfully, the resourceId is {0}".format(resource_id))