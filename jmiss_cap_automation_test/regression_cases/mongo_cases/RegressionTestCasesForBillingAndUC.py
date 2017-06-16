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
	price_info = query_mongo_db_price_step(config, instance_data, cap_http_client, instance_data["flavor_info"])
	info_logger.info("[INFO] The price of the mongo instance is %s", price_info)
	# 验证点，获取的价格信息与产品给出的价格信息一致

    # 获取mongo的折扣信息
    def test_query_min_discount(self, config, instance_data, cap_http_client):
        info_logger.info("[Scenario] Get the price info about the mongo instance")
        price_info = query_mongo_db_discount_step(config, instance_data, cap_http_client, instance_data["query_min_discount"])
        info_logger.info("[INFO] The discount of the mongo instance is %s", price_info)
	# 验证点，获取折扣信息与当前的折扣

    def test_user_quota(self, config, instance_data, cap_http_client):
	# 获取用户配额
	# 设置用户配额，已使用的配额为用户分配的最大配额
	# 创建mongo实例
	# 验证mongo实例创建失败
	# 获取用户配额
	# 验证用户配额没有变化
	# 修改用户配额，已用的减少，使用户可以创建mongo实例
	# 获取用户配额
	# 创建mongo实例
	# 获取用户配额
	# 验证，用户配额被占用1，即配额减去的数量为1
	# 删除创建的两个mongo实例
	# 获取用户配额，用户配额减少的数量为2
