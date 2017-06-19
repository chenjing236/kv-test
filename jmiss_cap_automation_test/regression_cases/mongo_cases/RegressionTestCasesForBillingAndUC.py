# -*- coding: utf-8 -*-

import pytest
import logging
import json
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
        request_id, coupons = query_available_coupons_step(config, instance_data, cap_http_client,instance_data["query_coupons"])
        print  len(coupons)


    #用户配额
    @pytest.mark.smoke
    def test_user_quota(self, config, instance_data, cap_http_client, mongo_http_client):
        info_logger.info("[Scenario] user quota")
        # 获取用户配额
        request_id,total,use=query_user_quota_step(config, instance_data, cap_http_client, "mongodb")
        # 设置用户配额，已使用的配额为用户分配的最大配额
        request_id=set_user_quota_step(config, instance_data, cap_http_client, "mongodb", 20)
        if 20!=use:
            request_id,total,use=modify_user_quota_step(config, instance_data, cap_http_client, "mongodb", 20-use)
        # 创建mongo实例
        # 验证mongo实例创建失败
        flag=False
        try:
            resource_id, mongo_info = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)
        except Exception as err:
            flag =True
        assert flag==True,"[ERROR] create mongo db is not a failure"

        # 获取用户配额
        request_id, total, use = query_user_quota_step(config, instance_data, cap_http_client,"mongodb")
        # 验证用户配额没有变化
        assert total == use, "[ERROR] the total does not equal the use"
        # 修改用户配额，已用的减少，使用户可以创建mongo实例
        request_id, total, use = modify_user_quota_step(config, instance_data, cap_http_client, "mongodb", -15)

        # 获取用户配额
        request_id, total, use = query_user_quota_step(config, instance_data, cap_http_client,"mongodb")
        # 创建mongo实例
        resource_id, mongo_info = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)
        # 获取用户配额
        request_id, total1, use1 = query_user_quota_step(config, instance_data, cap_http_client,"mongodb")
        # 验证，用户配额被占用1，即配额减去的数量为1
        assert use1 - use == 1, "[ERROR] the increase is not is 1,before:%s,after:%s".format(use, use1)
        # 创建mongo实例
        resource_id2, mongo_info = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)
        # 获取用户配额
        request_id, total2, use2 = query_user_quota_step(config, instance_data, cap_http_client, "mongodb")
        #删除创建的两个mongo实例
        spaceIds=[resource_id,resource_id2]
        request_id=delete_mongo_instances_step(config, instance_data, mongo_http_client,spaceIds)
        # 获取用户配额，用户配额减少的数量为2
        request_id, total3, use3 = query_user_quota_step(config, instance_data, cap_http_client, "mongodb")
        assert  use2-use3,"[ERROR] the increase is not is 2,before:%s,after:%s".format(use2, use3)