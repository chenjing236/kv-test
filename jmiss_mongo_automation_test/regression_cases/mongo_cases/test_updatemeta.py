# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestUpdatemeta:
    # 修改名称个
    @pytest.mark.smoke
    def test_change_name_of_mongo_instance(self,config, instance_data, http_client, create_mongo_instance):
	info_logger.info("[SCENARIO] Change the name for the mongo instance")
	# 创建mongo实例
	info_logger.info("[STEP] Create a mongo instance")
	space_id=create_mongo_instance
	info_logger.info("[INFO] The mongo instance %s is created", space_id)
	info_logger.info("[STEP] Change name for the mongo instance")
	name_changed = "SMOKE_TEST"
	change_name_for_mongo_instance_step(config, instance_data, http_client, space_id, name_changed)
	info_logger.info("[STEP] Get the name changed for the mongo instance %s", space_id)
	mongo_info = get_detail_info_of_instance_step(config, instance_data, http_client, space_id)
	info_logger.info("[VERIFICATION] The name changed is the same with the specific name, and the name is changed to %s", mongo_info["name"])
	assert name_changed == mongo_info["name"], "[ERROR] It is failed to change name for the mongo instance {0}".format(space_id)

    # 修改名称，修改名称为中文名称，验证中文字符不会乱码
    @pytest.mark.smoke
    def test_change_en_name_of_mongo_instance(self,config, instance_data, http_client, create_mongo_instance):
        info_logger.info("[SCENARIO] Change the name for the mongo instance")
        # 创建mongo实例
        info_logger.info("[STEP] Create a mongo instance")
        space_id=create_mongo_instance
        info_logger.info("[INFO] The mongo instance %s is created", space_id)
        info_logger.info("[STEP] Change name for the mongo instance")
        name_changed = "自动化测试用例"
        change_name_for_mongo_instance_step(config, instance_data, http_client, space_id, name_changed)
        info_logger.info("[STEP] Get the name changed for the mongo instance %s", space_id)
        mongo_info = get_detail_info_of_instance_step(config, instance_data, http_client, space_id)
        info_logger.info("[VERIFICATION] The name changed is the same with the specific name, and the name is changed to %s", mongo_info["name"])
        assert name_changed == mongo_info["name"], "[ERROR] It is failed to change name for the mongo instance {0}".format(space_id)
