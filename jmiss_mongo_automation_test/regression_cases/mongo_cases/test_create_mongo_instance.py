# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestCreateMongoInstance:

    # 创建不同规格的mongo实例，验证实际mongo对应的container的规格与创建时指定的规格一致
    @pytest.mark.smoke
    def test_create_mongo_instance_and_verify_flavor(self, config, instance_data, http_client, mysql_client, docker_client):
	try:
		info_logger.info("[SCENARIO] Create two mongo instances whith different flavors")
		# 获取flavor 1C_2M_4D_10E的flavor id
        	info_logger.info("[STEP] Get flavor id by flavor info for 1C_2M_4D_10E")
        	flavor_id_1 = get_flavorid_by_flavor_info_step(instance_data, http_client, "mongo_1C_2M_4D_10E")
        	info_logger.info("[INFO] Flavor id is %s", flavor_id_1)
        	assert flavor_id_1 != "", "[ERROR] Flavor id is none"
                # 获取flavor 2C_4M_8D_10E的flavor id
                info_logger.info("[STEP] Get flavor id by flavor info for 2C_4M_8D_10E")
                flavor_id_2 = get_flavorid_by_flavor_info_step(instance_data, http_client, "mongo_2C_4M_8D_10E")
                info_logger.info("[INFO] Flavor id is %s", flavor_id_2)
                assert flavor_id_2 != "", "[ERROR] Flavor id is none"
        	# 创建mongo实例，规格为1C_2M_4D_10E
        	info_logger.info("[STEP] Create a mongo instance with flavor 1C_2M_4D_10E")
        	space_id_1 = create_mongo_instance_with_flavor_step(config, instance_data, http_client, flavor_id_1)
		info_logger.info("[INFO] The mongo instance %s is going to be created", space_id_1)
		#查看mongo实例状态
		info_logger.info("[STEP] Get the status of the mongo instance %s", space_id_1)
		status_1 = get_status_of_instance_step(config, instance_data, http_client, space_id_1)
		info_logger.info("[INFO] The status of the mongo %s is %s", space_id_1, status_1)
		info_logger.info("[VERIFICATION] The status of the mongo instance %s is available", space_id_1)
		assert status_1 == 100, "[ERROR] Instance {0} is unavailable".format(space_id_1)
		# 获取创建mongo实例的操作结果,线上通过获取操作结果接口获取replica信息，测试环境通过instance表中获取mongo实例的拓扑信息
		info_logger.info("[STEP] Get the replica of the mongo instance %s", space_id_1)
		container_1, container_2, hidden = get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id_1)
		info_logger.info("[INFO] There are three containers for the mongo instance %s, %s, %s, %s", space_id_1, json.dumps(container_1), json.dumps(container_2), json.dumps(hidden))
		# 通过docker container获取规格信息
		info_logger.info("[STEP] Get the flavor info for the mongo instance %s", space_id_1)
		flavor_info_from_container = get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_1)
		info_logger.info("[INFO] The flavor info is %s", json.dumps(flavor_info_from_container))
        	# 验证规格信息
		info_logger.info("[INFO] The flavor info is cpu=%s, memory=%s, disk=%s", flavor_info_from_container["cpuInfo"]["num"], flavor_info_from_container["memInfo"]["total"], flavor_info_from_container["dataDisk"]["total"])
		perg= float(1024*1024*1024)
		disk_1 = math.ceil(float(flavor_info_from_container["dataDisk"]["total"]) / perg)
		memory_1 = float(flavor_info_from_container["memInfo"]["total"]) / perg
		assert 2 == int(memory_1), "[ERROR] Memmory is not 2G"
		assert 4 == int(disk_1), "[ERROR] Disk is not 4G"
        	# 创建mongo实例，规格为2C_4M_8D_10E
                info_logger.info("[STEP] Create a mongo instance with flavor 2C_4M_8D_10E")
                space_id_2 = create_mongo_instance_with_flavor_step(config, instance_data, http_client, flavor_id_2)
                info_logger.info("[INFO] The mongo instance %s is going to be created", space_id_1)
        	# 查看mongo实例状态
                info_logger.info("[STEP] Get the status of the mongo instance %s", space_id_2)
                status_2 = get_status_of_instance_step(config, instance_data, http_client, space_id_2)
                info_logger.info("[INFO] The status of the mongo %s is %s", space_id_2, status_2)
                info_logger.info("[VERIFICATION] The status of the mongo instance %s is available", space_id_2)
                assert status_2 == 100, "[ERROR] Instance {0} is unavailable".format(space_id_2)
        	# 通过docker container获取规格信息
                info_logger.info("[STEP] Get the replica of the mongo instance %s", space_id_2)
                container_2_1, container_2_2, hidden_2 = get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id_2)
                info_logger.info("[INFO] There are three containers for the mongo instance %s, %s, %s, %s", space_id_2, json.dumps(container_2_1), json.dumps(container_2_2), json.dumps(hidden_2))
                # 通过docker container获取规格信息
                info_logger.info("[STEP] Get the flavor info for the mongo instance %s", space_id_2)
                flavor_info_from_container_2 = get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_2_1)
                info_logger.info("[INFO] The flavor info is %s", json.dumps(flavor_info_from_container_2))
                # 验证规格信息
                info_logger.info("[INFO] The flavor info is cpu=%s, memory=%s, disk=%s", flavor_info_from_container_2["cpuInfo"]["num"], flavor_info_from_container_2["memInfo"]["total"], flavor_info_from_container_2["dataDisk"]["total"])
                perg= float(1024*1024*1024)
                disk_2 = math.ceil(float(flavor_info_from_container_2["dataDisk"]["total"]) / perg)
                memory_2 = float(flavor_info_from_container_2["memInfo"]["total"]) / perg
                assert 4 == int(memory_2), "[ERROR] Memmory is not 4G"
                assert 8 == int(disk_2), "[ERROR] Disk is not 8G"
	except Exception as e:
		assert False, "[ERROR] Exception is %s".format(e)
	finally:
		if None == space_id_1:
			assert False, "[ERROR] The mongo instance1 cannot be created"
		if None == space_id_2:
			assert False, "[ERROR] The mongo instance2 cannot be created"
		# 删除mongo实例
		info_logger.info("[STEP] Delete the mongo instance %s", space_id_1)
		delete_instance_step(config, instance_data, http_client, space_id_1)
		# 删除规格2C_4M_8D_10E
		info_logger.info("[STEP] Delete the mongo instance %s", space_id_2)
		delete_instance_step(config, instance_data, http_client, space_id_2)

    #创建mongo实例，验证mongo实例创建成功后，数据库中的信息正确	
    def _create_mongo_instance_and_verify_data(self, config, instance_data, http_client, mysql_client,):
	info_logger.info("[SCENARIO] Create a mongo instance and verify that the data of the mongo created is correct")

