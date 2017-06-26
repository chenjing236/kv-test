# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestClustersByPage:
    #分页查看列表信息
    @pytest.mark.smoke
    def test_get_clusters_by_page(self, config, instance_data, http_client):
	try:
		info_logger.info("[SCENARIO] Get the clusters by page")
		# 创建mongo实例1
		info_logger.info("[STEP] Create a mongo instance 1")
		space_id_1=create_available_mongo_instance_step(config, instance_data, http_client)
		info_logger.info("[INFO] The mongo instance %s is created", space_id_1)
		# 修改mongo实例名称
		mongo_info_1=get_changed_name_of_mongo_instance_step(config, instance_data, http_client, space_id_1, "SMOKE_TEST_1")
		info_logger.info("[INFO] The name of the mongo instance %s is changed to %s", space_id_1, mongo_info_1["name"])
		# 创建mongo实例2
		info_logger.info("[STEP] Create a mongo instance 2")
        	space_id_2=create_available_mongo_instance_step(config, instance_data, http_client)
        	info_logger.info("[INFO] The mongo instance %s is created", space_id_2)
        	# 修改mongo实例名称
        	mongo_info_2=get_changed_name_of_mongo_instance_step(config, instance_data, http_client, space_id_2, "SMOKE_TEST_2")
        	info_logger.info("[INFO] The name of the mongo instance %s is changed to %s", space_id_2, mongo_info_2["name"])
		# 创建mongo实例3
        	info_logger.info("[STEP] Create a mongo instance 3")
        	space_id_3=create_available_mongo_instance_step(config, instance_data, http_client)
        	info_logger.info("[INFO] The mongo instance %s is created", space_id_3)
        	# 修改mongo实例名称
        	mongo_info_3=get_changed_name_of_mongo_instance_step(config, instance_data, http_client, space_id_3, "SMOKE_TEST_3")
        	info_logger.info("[INFO] The name of the mongo instance %s is changed to %s", space_id_3, mongo_info_3["name"])
		# 分页查询，每页1个实例，按名称倒序排列
		info_logger.info("[STEP] Get the mongo instance in the frist page")
		space_in_page_1=get_clusters_by_page_step(config, instance_data, http_client, "SMOKE_TEST", 1, 1)
		# 验证第一页是mongo3
		info_logger.info("[INFO] The mongo instance is %s in first page", json.dumps(space_in_page_1))
		assert "SMOKE_TEST_3" == space_in_page_1["spaces"][0]["name"]
		# 验证第二页是mongo2
        	info_logger.info("[STEP] Get the mongo instance in the secondary page")
        	space_in_page_2=get_clusters_by_page_step(config, instance_data, http_client, "SMOKE_TEST", 1, 2)
        	info_logger.info("[INFO] The mongo instance is %s in secondary page", json.dumps(space_in_page_2))
		assert "SMOKE_TEST_2" == space_in_page_2["spaces"][0]["name"]
	
		# 验证第三页是mongo1
        	info_logger.info("[STEP] Get the mongo instance in the third page")
        	space_in_page_3=get_clusters_by_page_step(config, instance_data, http_client, "SMOKE_TEST", 1, 3)
        	info_logger.info("[INFO] The mongo instance is %s in third page", json.dumps(space_in_page_3))
		assert "SMOKE_TEST_1" == space_in_page_3["spaces"][0]["name"]
	except Exception as e:
		assert False, "[ERROR] Exception is %s".format(e)
	finally:
		# 删除mongo实例1
		info_logger.info("[STEP] Delete the mongo instance %s", space_id_1)
		delete_instance_step(config, instance_data, http_client, space_id_1)
		info_logger.info("[INFO] The mongo instance %s is deleted", space_id_1)
		# 删除mongo实例2
        	info_logger.info("[STEP] Delete the mongo instance %s", space_id_2)
        	delete_instance_step(config, instance_data, http_client, space_id_2)
        	info_logger.info("[INFO] The mongo instance %s is deleted", space_id_2)
		# 删除mongo实例3
        	info_logger.info("[STEP] Delete the mongo instance %s", space_id_3)
        	delete_instance_step(config, instance_data, http_client, space_id_3)
        	info_logger.info("[INFO] The mongo instance %s is deleted", space_id_3)

