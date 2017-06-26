# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestDeleteMongoInstance:
    #删除mongo实例
    @pytest.mark.smoke
    def test_delete_mongo_instance(self, config, instance_data, http_client, mysql_client, docker_client):
	info_logger.info("[SCENARIO] Delete a mongo instance")
	# 创建mongo实例
	info_logger.info("[STEP] Create a mongo instance")
	space_id=space_id = create_mongo_instance_step(config, instance_data, http_client)
	info_logger.info("[STEP] Get status of the mongo instance %s", space_id)
	status = get_status_of_instance_step(config, instance_data, http_client, space_id)
	info_logger.info("[INFO] The status of the mongo %s is %s", space_id, status)
	#从数据库的instance表中查询mongo的instance信息
	container_1, container_2, hidden = get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id)
	# mongo的primary container，secondary container, hidden container存在于物理资源机上
	is_alive =  ping_container_step(config, instance_data, http_client, docker_client, container_1)
	assert "true" == is_alive, "[ERROR] The container [{0}] is not alive or not exited".format(container_1["docker_id"])
	info_logger.info("[INFO] The status of the container [%s] is aliv", container_1["docker_id"])
	# 删除mongo实例
	info_logger.info("[STEP] Delete the mongo instance %s", space_id)
        delete_instance_step(config, instance_data, http_client, space_id)
	time.sleep(int(instance_data["wait_time"]))
	status_for_delete_instance = get_status_of_deleted_instance_step(config, instance_data, http_client, space_id)
	assert 102 == status_for_delete_instance, "[ERROR] The mongo instance [{0}] cannot be deleted".format(space_id)
	# 验证通过物理资源机查看mongo实例对应的container已经不存在
	is_alive =  ping_container_step(config, instance_data, http_client, docker_client, container_1)
	assert "false" == is_alive, "[ERROR] The container [{0}] is not alive or not exited".format(container_1["docker_id"])
