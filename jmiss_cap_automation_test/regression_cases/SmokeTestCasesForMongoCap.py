# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoCap:
    # 创建制定规格mongo实例，类型为按配置
    @pytest.mark.smoke
    def test_create_an_instance(self, config, instance_data, create_mongo_instance):
        info_logger.info("[Scenario] Create an instance for mongo, the instance consists of a primary container, a secondary container and a hidden container")
	# 创建mongo实例
        resource_id, mongo_info = create_mongo_instance
        info_logger.info("[INFO] The mongo instance %s is created", resource_id)
	# mongo实例的flavor信息
	info_logger.info("[STEP] Get the flavor info of the mongo instance %s", resource_id)
	flavor_info = mongo_info["flavor"]
	# 验证mongo实例的flavor信息与创建时传入的flavor信息一致，包括cpu，memory，disk, iops, maxConn
	info_logger.info("[VERIFICATION] The falvor info is the same with setted up flavor info")
	assert instance_data["create_mongo_db"]["cpu"] == flavor_info["cpu"] and instance_data["create_mongo_db"]["memory"] == flavor_info["memory"] and instance_data["create_mongo_db"]["disk"] == flavor_info["disk"] and instance_data["create_mongo_db"]["iops"] == flavor_info["iops"] and instance_data["create_mongo_db"]["maxLink"] == flavor_info["maxConn"], "[ERROR] The flavor info is not {0}".format(json.dumps(flavor_info))

    # 修改mongo实例名称
    def test_modify_name_for_mongo_instance(self, config, instance_data, mongo_http_client, create_mongo_instance):
	info_logger.info("[Scenario] Modify the name of the mongo instance")
	# 创建mongo实例
	resource_id, mongo_info = create_mongo_instance
	info_logger.info("[INFO] The mongo instance %s is created", mongo_info["spaceId"])
	# 修改mongo实例名称
	info_logger.info("[STEP] Modify name of the mongo instance")
	modify_mongo_db_name_step(config, instance_data, mongo_http_client, mongo_info["spaceId"], "mongo_instance")
	# 获取mongo实例详情
	info_logger.info("[STEP] Get the detail info of the mongo instance including the modified name")
	request_id, mongo_info_modified = query_mongo_db_detail_step(config, instance_data, mongo_http_client, mongo_info["spaceId"])
	# 验证mongo实例详情中的mongo的名字与修改名字一致
	info_logger.info("[VERIFICATION] The modified name for the mongo instance is correct")
	assert "mongo_instance" == mongo_info_modified["name"], "[ERROR] It is failed to modify the name of mongo instance {0}".format(mongo_info["spaceId"])

    # 获取flaovr规格信息
    def test_get_flavor_info(self, config, instance_data, mongo_http_client, create_mongo_instance):
	info_logger.info("[Scenario] Modify the name of the mongo instance")
        # 创建mongo实例
        resource_id, mongo_info = create_mongo_instance
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info["spaceId"])
	# 获取mongo实例的flavor信息
	info_logger.info("[STEP] Get the flavor info of the mongo instance %s", resource_id)
	flavor_info = mongo_info["flavor"]
	# 查询flavor列表
	info_logger.info("[STEP] Get the flavor info list")
	request_id, flavor_info_list = get_flavor_list_step(config, instance_data, mongo_http_client)
	flavor_info_list_str = json.dumps(flavor_info_list)
	# 验证mongo实例的flavor信息在flavor列表中
	info_logger.info("[VERIFICATION] The flavor info of the mongo instance is in the flavor info list")
	mongo_flavor_info = {"diskStep":10, "minDisk":instance_data["create_mongo_db"]["disk"], "iops":instance_data["create_mongo_db"]["iops"], "maxLink":instance_data["create_mongo_db"]["maxLink"], "memory":instance_data["create_mongo_db"]["memory"], "cpu":instance_data["create_mongo_db"]["cpu"], "maxDisk":200}
	mongo_flavor_info_str = json.dumps(mongo_flavor_info)
	is_flavor_in = "false"
	if mongo_flavor_info_str not in flavor_info_list_str:
		is_flavor_in = "false"
	else:
		is_flavor_in = "true"
	assert "true" == is_flavor_in, "[ERROR]The flavor info of the mongo instance {0} is not in flavor list".format(resource_id)
