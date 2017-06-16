# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestRegressionCasesForMongoCap:
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

    # 查看mongo列表信息
    def test_query_mongo_dbs(self, config, instance_data, mongo_http_client, create_mongo_instance):
	# 查看mongo实例列表
	# 创建mongo实例，类型为按配置
	# 查看mongo实例列表
	# 验证创建的mongo实例在列表中

    # 过滤查询mongodb列表信息
    def test_query_filter_mongo_dbs(self, config, instance_data, mongo_http_client):
	# 按照资源状态过滤创建成功的资源, 按照资源名称排序，每页1个资源，3页
	# 创建mongo资源
	# 修改名称，名称为mongo_instance1
	# 创建mongo资源
	# 修改名称, 名称为mongo_instance2
	# 创建mongo资源
	# 修改名称, 名称为mongo_instance3
	# 过滤mongo实例列表，按照资源状态过滤创建成功的资源, 按照资源名称排序，每页1个资源，3页
	# 验证第一页为mongo_instance_1，且数量为1
	# 验证第二页为mongo_instance_2，且数量为1
	# 验证第三页为mongo_instance_3，且数量为1

    # 批量删除
    def test_delete_mongo_dbs(self, config, instance_data, mongo_http_client):
	# 创建mongo实例1
	# 创建mongo实例2
	# 创建mongo实例3
	# 查询mongo实例列表
	# 验证mongo1,mongo2,mongo3都在实例列表中
	# 批量删除mongo1，mongo3,
	# 查询mongo实例列表
	# 验证mongo1和mongo3不在mongo实例列表中，mongo2在实例列表中

    # 获取拓扑结构
    def test_query_mongo_db_topology(self, config, instance_data, mongo_http_client, create_mongo_instance):
	# 创建mongo实例
	# 获取拓扑结构
	# 验证拓扑结构有primary，secondary，hidden信息，且信息不为空

    # 获取vpc列表及subnet的列表信息
    def test_vpc_and_subnet_list(self, config, instance_data, mongo_http_client):
	# 选择subnet及对应的vpc，创建mongo实例
	# 获取mongo实例信息中的vpc和subnet信息
	# 获取vpc信息
	# 获取subnet信息
	# 验证，vpc和subnet信息与指定的vpc和subnet信息一致

    # 查询监控信息
    def test_query_monitor_info(self, config, instance_data, mongo_http_client, create_mongo_instance):
	# 创建mongo实例
	# 获取mongo实例的监控信息
	# 验证监控信息项都存在

    # 查询实时信息
    def test_query_mongo_db_real_time_info(self, config, instance_data, mongo_http_client, create_mongo_instance):
	# 创建mongo实例
	# 获取mongo实例的实时监控信息
	# 验证监控项都存在
