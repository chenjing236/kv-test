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
    @pytest.mark.smoke
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
    @pytest.mark.smoke
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
	# 验证mongo实例的flavor信息在flavor列表中
	info_logger.info("[VERIFICATION] The flavor info of the mongo instance is in the flavor info list")
	mongo_flavor_info = {"diskStep":1, "minDisk":instance_data["create_mongo_db"]["disk"], "iops":instance_data["create_mongo_db"]["iops"], "maxLink":instance_data["create_mongo_db"]["maxLink"], "memory":instance_data["create_mongo_db"]["memory"], "cpu":instance_data["create_mongo_db"]["cpu"], "maxDisk":10}
	is_flavor_exited = is_exited_in_flavor_list_step(flavor_info_list, instance_data["create_mongo_db"])
	assert True == is_flavor_exited, "[ERROR]The flavor info of the mongo instance {0} is not in flavor list".format(resource_id)

    # 过滤查询mongodb列表信息
    @pytest.mark.smoke
    def test_query_filter_mongo_dbs(self, config, instance_data, mongo_http_client, create_three_mongo_instances):
        # 按照资源状态过滤创建成功的资源, 按照资源名称排序，每页1个资源，3页
	info_logger.info("[SCENARIO] Filter the mongo info from the list of mongo instance by filter condition")
        # 修改名称, 名称为mongo_instance1
	info_logger.info("[STEP] Create three mongo instances")
        resource_id1, mongo_info1,resource_id2, mongo_info2,resource_id3, mongo_info3 = create_three_mongo_instances
	info_logger.info("[STEP] Change name of the mongo instance to mongo_instance1")
        modify_mongo_db_name_step(config, instance_data, mongo_http_client, mongo_info1["spaceId"], "mongo_instance1")
	info_logger.info("[STEP] Change name of the mongo instance to mongo_instance2")
        modify_mongo_db_name_step(config, instance_data, mongo_http_client, mongo_info2["spaceId"], "mongo_instance2")
	info_logger.info("[STEP] Change name of the mongo instance to mongo_instance3")
        modify_mongo_db_name_step(config, instance_data, mongo_http_client, mongo_info3["spaceId"], "mongo_instance3")
	info_logger.info("[VERIFICATION] Filter mongo instance by name and there is an instance per page")
        request_id, total, list = get_filter_mongo_dbs_step(config, instance_data, mongo_http_client, "mongo_instance",1)
        assert len(list) == 1, "[ERROR] The filter mongo list's size is not 1"
	assert "mongo_instance3" == list[0]["name"], "[ERROR] It is failed to sort mongo instance by name"

        request_id, total, list = get_filter_mongo_dbs_step(config, instance_data, mongo_http_client, "mongo_instance",2)
        assert len(list) == 1, "[ERROR] The filter mongo list's size is not 1"
	assert "mongo_instance2" == list[0]["name"], "[ERROR] It is failed to sort mongo instance by name"

        request_id, total, list = get_filter_mongo_dbs_step(config, instance_data, mongo_http_client, "mongo_instance",3)
        assert len(list) == 1, "[ERROR] The filter mongo list's size is not 1"
	assert "mongo_instance1" == list[0]["name"], "[ERROR] It is failed to sort mongo instance by name"

    # 批量删除
    def test_delete_mongo_dbs(self, config, instance_data, mongo_http_client, cap_http_client):
        info_logger.info("[Scenario] Delete mongos instance")
        # 创建mongo实例1
        resource_id1, mongo_info1 = create_mongo_instance_with_params_step(config, instance_data, mongo_http_client, cap_http_client)
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info1["spaceId"])

        # 创建mongo实例2
        resource_id2, mongo_info2 = create_mongo_instance_with_params_step(config, instance_data, mongo_http_client, cap_http_client)
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info2["spaceId"])

        # 创建mongo实例3
        resource_id3, mongo_info3 = create_mongo_instance_with_params_step(config, instance_data, mongo_http_client, cap_http_client)
        info_logger.info("[INFO] The mongo instance %s is created", mongo_info3["spaceId"])

        # 查询mongo实例列表
        request_id, list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证mongo1,mongo2,mongo3都在实例列表中
        flag1 = False
        flag2 = False
        flag3 = False
        for item in list:
            if item["spaceId"] == resource_id1:
                flag1 = True
            elif item["spaceId"] == resource_id2:
                flag2 = True
            elif item["spaceId"] == resource_id3:
                flag3 = True
        assert flag1 == True and flag2 == True and flag3 == True, "[ERROR] create mongo dbs failure"

        # 批量删除mongo1，mongo3,
        spaceIds = [resource_id1, resource_id3]
        request_id = delete_mongo_instances_step(config, instance_data, mongo_http_client, spaceIds)
        time.sleep(5)

        while(query_mongo_db_detail_error_step(config, instance_data, mongo_http_client, resource_id1)):
            time.sleep(5)
        while (query_mongo_db_detail_error_step(config, instance_data, mongo_http_client, resource_id3)):
            time.sleep(5)

        # 验证mongo1和mongo3不在mongo实例列表中，mongo2在实例列表中
        # 查询mongo实例列表
        request_id, list = get_mongo_dbs_step(config, instance_data, mongo_http_client)

        flag1 = False
        flag2 = False
        flag3 = False
        for item in list:
            if item["spaceId"] == resource_id1:
                flag1 = True
                continue
            elif item["spaceId"] == resource_id2:
                flag2 = True
                continue
            elif item["spaceId"] == resource_id3:
                flag3 = True
                continue
        assert flag1 == False and flag2 == True and flag3 == False, "[ERROR] The delete mongo dbs failed"
        spaceIds = [resource_id2]
        request_id = delete_mongo_instances_step(config, instance_data, mongo_http_client, spaceIds)
