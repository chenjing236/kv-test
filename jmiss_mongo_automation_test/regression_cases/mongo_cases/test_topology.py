# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestTopology:
    # 创建mongo实例，验证实际mongo对应的container的副本集关系与创建时设置的副本集关系一致
    @pytest.mark.smoke 
    def test_create_mongo_instance_and_verify_replica(self, config, instance_data, http_client, mysql_client, docker_client, create_mongo_instance):
	info_logger.info("[SCENARIO] Create a mongo instance that consists of a primary container, a secondary container and a hidden container")
	# 创建mongo实例
	info_logger.info("[STEP] Create a mongo instance")
	space_id=create_mongo_instance
	info_logger.info("[INFO] The mongo instance %s is created", space_id)
	info_logger.info("[STEP] Get the replica of the mongo instance %s", space_id)
        container_1, container_2, hidden = get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id)
	# 获取mongo实例的副本集信息
	info_logger.info("[STEP] Get replica info for the mongo instance %s", space_id)
	topology_info = get_topology_of_mongo_step(config, instance_data, http_client, space_id)
	primary = topology_info["primary"]["ip"] + ":" + str(topology_info["primary"]["port"])
	secondary = topology_info["secondary"][0]["ip"] + ":" + str(topology_info["secondary"][0]["port"])
	hidden = topology_info["hidden"][0]["ip"] + ":" + str(topology_info["hidden"][0]["port"])
	info_logger.info("[INFO] The replica info is [primary: %s], [sencondary: %s], [hidden: %s]", primary, secondary, hidden)
	# 通过mongo的container获取mongo的副本集信息
	info_logger.info("[STEP] Get replica info for the container [%s] of the mongo", container_1["docker_id"])
	replica_info = get_replica_info_from_container(config, instance_data, http_client, docker_client, container_1)
	primary_info = replica_info["primary"]
	secondary_info = replica_info["secondary"][0]
	hidden_info = replica_info["hidden"][0]
	info_logger.info("[INFO] The replica info from container is [primary: %s], [sencondary: %s], [hidden: %s]", primary_info, secondary_info, hidden_info)
	# 验证副本集
	info_logger.info("[VERIFCATION] The replicat info from the mongo instance is in accordance with the replicat info from container")
	assert primary == primary_info, "[ERROR] The primary info of the mongo instance is not the same with the primary info of the container"
	assert secondary == secondary_info, "[ERROR] The secondary info of the mongo instance is not the same with the secondary info of the container"
	assert hidden == hidden_info, "[ERROR] The hidden info of the mongo instance is not the same with the hidden info of the container"
