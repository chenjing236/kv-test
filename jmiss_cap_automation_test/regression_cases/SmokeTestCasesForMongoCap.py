# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoCap:
    # 创建制定规格mongo实例，类型为按配置
    @pytest.mark.smoke
    def test_create_an_instance(self, config, data_for_instance, create_mongo_instance):
        info_logger.info("[Scenario] Create an instance for mongo, the instance consists of a primary container, a secondary container and a hidden container")
	# 创建mongo实例
        mongo_info = create_mongo_instance_step
	mongo_info_obj = json.loads(mongo_info)
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info_obj["spaceId"])
	# mongo实例的flavor信息
	#flavor_info = mongo_info_obj["flavor"]
	# 验证mongo实例的flavor信息与创建时传入的flavor信息一致，包括cpu，memory，disk, iops, maxConn
	#assert data_for_instance["create_mongo_db"]["cpu"] == flavor_info["cpu"] and data_for_instance["create_mongo_db"]["memory"] == flavor_info["memory"] and data_for_instance["create_mongo_db"]["disk"] == flavor_info["disk"] and data_for_instance["create_mongo_db"]["iops"] == flavor_info["iops"] and data_for_instance["create_mongo_db"]["maxLink"] == flavor_info["maxConn"], "[ERROR] The flavor info is not {0}".format(json.dumps(flavor_info))

    # 修改mongo实例名称
    def _modify_name_for_mongo_instance(self, config, data_for_instance, mongo_http_client, create_mongo_instance):
	info_logger.info("[Scenario] Modify the name of the mongo instance")
	# 创建mongo实例
	mongo_info = create_mongo_instance_step
	info_logger.info("[INFO] The mongo instance %s is created", mongo_info["spaceId"])
	# 修改mongo实例名称
	modify_mongo_db_name_step(config, data_for_instance, mongo_info["space_id"], "verification_for_modifying_mongo_name")
	# 获取mongo实例详情
	mongo_info_modified = query_mongo_db_detail_step(config, instance_data, mongo_http_client, mongo_info["spaceId"])
	# 验证mongo实例详情中的mongo的名字与修改名字一致
	assert "verification_for_modifying_mongo_name" == mongo_info_modified["name"], "[ERROR] It is failed to modify the name of mongo instance {0}".format(mongo_info["spaceId"])

    # 获取flaovr规格信息
    def _get_flavor_info(self, config, data_for_instance, create_mongo_instance):
	info_logger.info("[Scenario] Modify the name of the mongo instance")
        # 创建mongo实例
        mongo_info = create_mongo_instance_step
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info["spaceId"])
	# 获取mongo实例的flavor信息
	# 查询flavor列表
	# 验证mongo实例的flavor信息在flavor列表中
