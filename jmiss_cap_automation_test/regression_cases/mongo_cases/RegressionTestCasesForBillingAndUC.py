# -*- coding: utf-8 -*-

import pytest
import logging

from BasicTestCase import *

info_logger = logging.getLogger(__name__)

# 提供给计费和UC的接口的测试用例
class TestRegressionCasesForBillingAndUC:
    # 获取mongo每种规格对应的价格信息
    @pytest.mark.smoke
    def test_query_mongo_db_price(self, config, instance_data, cap_http_client):
	info_logger.info("[Scenario] Get the price info about the mongo instance")
	info_logger.info("[STEP] Get the price info of the mongo")
	request_id, price_info = query_mongo_db_price_step(config, instance_data, cap_http_client, instance_data["flavor_info_according_configration"])
	info_logger.info("[INFO] The price of the mongo instance is %s", json.dumps(price_info))
	#验证点，获取的价格信息与产品给出的价格信息一致
	info_logger.info("[VERIFICATION] The price of the mongo is the same with the setted up price")
	assert instance_data["flavor_info_according_configration"]["price"] == price_info["price"], "[ERROR] The price for the flavor {0} is not same whith the price of the mongo".format(json.dumps(price_info))

    # 获取mongo的折扣信息
    def test_query_min_discount(self, config, instance_data, cap_http_client):
        info_logger.info("[Scenario] Get the price info about the mongo instance")
	info_logger.info("[STEP] Get the discount info of the mongo")
        request_id, discount_info = query_query_min_discount_step(config, instance_data, cap_http_client, instance_data["query_min_discount_according_configration"])
        info_logger.info("[INFO] The discount of the mongo instance is %s", json.dumps(discount_info))
	# 验证点，获取折扣信息与当前的折扣
	info_logger.info("[VERIFICATION] The discount info of the mongo is the same with the setted up discount")
	assert instance_data["query_min_discount_according_configration"]["discount"] == discount_info["discount"], "[ERROR] The discount for the discount type {0} is not same whith the price of the mongo".format(json.dumps(discount_info))

    #获取用户优惠券
    def test_query_available_coupons(self, config, instance_data, cap_http_client):
        info_logger.info("[Scenario] Query available coupons")
        request_id, coupons = query_available_coupons_step(config, instance_data, cap_http_client,
        instance_data["query_available_coupons"])
        print len(coupons)

    #用户配额
    def test_user_quota(self, config, instance_data, cap_http_client,mongo_http_client,create_mongo_instance):
        info_logger.info("[Scenario] user quota")
        # 获取用户配额
        request_id,total,use=query_user_quota_step(config, instance_data, cap_http_client, instance_data["user_quota"])
        # 设置用户配额，已使用的配额为用户分配的最大配额
        request_id=set_user_quota_step(config, instance_data, http_client, instance_data["user_quota"], 20)
        request_id,total,use=modify_user_quota_step(config, instance_data, http_client, resource, 20)
        # 创建mongo实例
        resource_id, mongo_info = create_mongo_instance
        # 验证mongo实例创建失败
        request_id, mongo_detail=query_mongo_db_detail_step(config, instance_data, mongo_http_client, resource_id)
        assert  mongo_detail["status"]==101,"[ERROR] the mongo db status is not 101"
        # 获取用户配额
        request_id,total,use=query_user_quota_step(config, instance_data, cap_http_client, instance_data["user_quota"])
        # 验证用户配额没有变化
        assert  total==use,"[ERROR] the total does not equal the use"
        # 修改用户配额，已用的减少，使用户可以创建mongo实例
        request_id,total,use=modify_user_quota_step(config, instance_data, http_client, resource, 15)
        # 获取用户配额
        request_id,total,use=query_user_quota_step(config, instance_data, cap_http_client, instance_data["user_quota"])
        # 创建mongo实例
        resource_id, mongo_info = create_mongo_instance
        # 获取用户配额
        request_id,total1,use1=query_user_quota_step(config, instance_data, cap_http_client, instance_data["user_quota"])
        # 验证，用户配额被占用1，即配额减去的数量为1
        assert  use1-use==1,"[ERROR] the reduce is not is 1,before:%s,after:%s".format(use,use1)
        # 删除创建的两个mongo实例
        resource_id, mongo_info = create_mongo_instance
        # 获取用户配额，用户配额减少的数量为2
        request_id, total2, use2 = query_user_quota_step(config, instance_data, cap_http_client,instance_data["user_quota"])
        assert  use2-use==2,"[ERROR] the reduce is not is 2,before:%s,after:%s".format(use,use2)

