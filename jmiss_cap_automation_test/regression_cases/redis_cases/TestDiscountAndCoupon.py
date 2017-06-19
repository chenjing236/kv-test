# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestDiscountAndCoupon:

    @pytest.mark.smoke
    def test_discount_and_coupon(self, config, instance_data, cap_http_client,create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))

        #调用中间层获取用户折扣接口，调用接口成功，正确返回用户折扣，验证其返回用户相应折扣（无法验证折扣正确性）
        fee_type = 1
        query_lowest_discount_step(redis_cap, fee_type)
        info_logger.info("[INFO] Test  successfully!")


        #调用中间层获取用户代金券，调用接口成功，正确返回用户的代金券列表（无法验证代金券正确性，线上用户支付需要使用代金券！）
        query_available_coupons_step(config, instance_data, cap_http_client, instance_data['redis_coupon_info'])

        info_logger.info("[INFO] Test queryAvailableCoupons successfully!")