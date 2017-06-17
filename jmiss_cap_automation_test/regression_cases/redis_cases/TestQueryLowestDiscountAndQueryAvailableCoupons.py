# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryLowestDiscountAndQueryAvailableCoupons:

    @pytest.mark.smoke
    def test_query_lowest_discount_and_query_available_coupons(self, create_redis_instance):
        #创建云缓存资源
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
        #调用运营停止资源接口