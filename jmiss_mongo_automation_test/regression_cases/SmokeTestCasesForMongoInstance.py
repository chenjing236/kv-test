# -*- coding: utf-8 -*- 

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoInstance:

    # 创建不同规格的mongo实例，验证实际mongo对应的container的规格与创建时指定的规格一致
    @pytest.mark.smoke
    def test_create_mongo_instance_and_verify_flavor(self, request, config, instance_data, http_client, mysql_client, docker_client):
	info_logger.info("[SCENARIO] Create two mongo instances whith different flavors")
	# 获取flavor 1C_2M_4D_10E的flavor id
        info_logger.info("[STEP] Get flavor id by flavor info")
        flavor_id_1 = get_flavorid_by_flavorinfo_step(instance_data, http_client)
        info_logger.info("[INFO] Flavor id is %s", flavor_id_1)
        assert flavor_id_1 != "", "[ERROR] Flavor id is none"

        # 创建mongo实例，规格为1C_2M_4D_10E
        info_logger.info("[STEP] Create a mongo instance")
        space_id_1, operation_id_1 = create_mongo_instance_with_flavor_step(config, instance_data, http_client, flavor_id_1)
	info_logger.info("[INFO] The mongo instance %s is going to be created, and the operation id is %s", space_id_1, operation_id_1)

	# 获取flavor 1C_2M_4D_10E的flavor id
	info_logger.info("[STEP] Get flavor id by flavor info")
	flavor_id_1 = get_flavorid_by_flavorinfo_step(instance_data, http_client)
	info_logger.info("[INFO] Flavor id is %s", flavor_id_1)
	#查看mongo实例状态
	info_logger.info("[STEP] Get the status of the mongo instance %s", space_id_1)
	status_1 = get_status_of_instance_step(config, instance_data, http_client, space_id_1)
	info_logger.info("[INFO] The status of the mongo %s is %s", space_id_1, status_1)
	info_logger.info("[VERIFICATION] The status of the mongo instance %s is available", space_id_1)
	assert status_1 == 100, "[ERROR] Instance {0} is unavailable".format(space_id_1)

	# 获取创建mongo实例的操作结果,线上通过获取操作结果接口获取replica信息，测试环境通过instance表中获取mongo实例的拓扑信息
	info_logger.info("[STEP] Get the replica of the mongo instance %s", space_id_1)
	#results_of_operation = get_results_of_operation_step(config, instance_data, http_client, space_id_1, operation_id_1)
	container_1, container_2, hidden = get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id_1)
	info_logger.info("[INFO] There are three containers for the mongo instance %s, %s, %s, %s", space_id_1, container_1, container_2, hidden)
	# 通过docker container获取规格信息
	info_logger.info("[STEP] Get the flavor info for the mongo instance %s", space_id_1)
	flavor_info_from_container = get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_1)
	info_logger.info("[INFO] The flavor info is %s", flavor_info_from_container)
        # 验证规格信息
        # 创建mongo实例，规格为2C_4M_8D_10E
        # 查看mongo实例状态
        # 通过docker container获取规格信息
	# 删除mongo实例
	info_logger.info("[STEP] Delete the mongo instance %s", space_id_1)
	delete_instance_step(config, instance_data, http_client, space_id_1)
	# 删除规格2C_4M_8D_10E

    # 创建mongo实例，验证实际mongo对应的container的副本集关系与创建时设置的副本集关系一致 
    def _create_mongo_instance_and_verify_replica(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Create a mongo instance that consists of a primary container, a secondary container and a hidden container")
	# 获取mongo实例的副本集信息
	# 通过mongo的container获取mongo的副本集信息
	# 验证副本集关系

    # 创建mongo实例，验证通过绑定外网IP的VM访问mongo实例，可以执行读写操作
    def _access_mongo_instance(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Access a mongo instance with a VM that binds a internet IP")
	# 获取mongo实例的domain信息
        # 通过VM访问mongo实例
        # 对mongo实例执行写操作
        # 获取写入mongo实例的数据

    # 创建mongo实例，验证stop mongo三个containers触发failover，failover执行完成后，mongo的状态为可用状态，副本集关系为primary, sencondary和hidden
    def _falover_mongo_containers(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Failover the primary container, the secondary container and the hidden container for the mongo instance")
	# 获取mongo的副本集关系
	# 同时stop mongo实例的三个containers,触发failover
	# 获取failover的操作结果，即查看failover是否完成，及完成的状态
	# 获取mongo的副本集关系

   #def _flavor_info(self, config, instance_data, http_client):
	# info_logger.info("[SCENARIO] Verify flavor info is the same with flavor id")
	# 根据flavor info获取flavor id
	# 根据flavor id获取flavor info的信息与stpe1的flavor信息一致

    def _delete_mongo_instance(self, config, instance_data, http_client):
	info_logger.info("[SCENARIO] Delete a mongo instance")
	# 创建mongo实例
	# 查看mongo实例状态，资源可用
	# mongo的primary container，secondary container, hidden container存在于物理资源机上
	# 删除mongo实例
	# 验证通过物理资源机查看mongo实例对应的container已经不存在
