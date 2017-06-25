# -*- coding: utf-8 -*- 

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoInstance:

    # 创建不同规格的mongo实例，验证实际mongo对应的container的规格与创建时指定的规格一致
    @pytest.mark.smoke
    def _create_mongo_instance_and_verify_flavor(self, config, instance_data, http_client, mysql_client, docker_client):
	info_logger.info("[SCENARIO] Create two mongo instances whith different flavors")
	# 获取flavor 1C_2M_4D_10E的flavor id
        info_logger.info("[STEP] Get flavor id by flavor info")
        flavor_id_1 = get_flavorid_by_flavorinfo_step(instance_data, http_client)
        info_logger.info("[INFO] Flavor id is %s", flavor_id_1)
        assert flavor_id_1 != "", "[ERROR] Flavor id is none"

        # 创建mongo实例，规格为1C_2M_4D_10E
        info_logger.info("[STEP] Create a mongo instance")
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
	info_logger.info("[INFO] There are three containers for the mongo instance %s, %s, %s, %s", space_id_1, container_1, container_2, hidden)
	# 通过docker container获取规格信息
	info_logger.info("[STEP] Get the flavor info for the mongo instance %s", space_id_1)
	#flavor_info_from_container = get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_1)
	flavor_info_from_container = get_flavor_info_using_mongo_agent_step(config, instance_data, http_client, container_1)
	info_logger.info("[INFO] The flavor info is %s", flavor_info_from_container)
        # 验证规格信息
        # 创建mongo实例，规格为2C_4M_8D_10E
        # 查看mongo实例状态
        # 通过docker container获取规格信息
	# 删除mongo实例
	info_logger.info("[STEP] Delete the mongo instance %s", space_id_1)
	delete_instance_step(config, instance_data, http_client, space_id_1)
	# 删除规格2C_4M_8D_10E

    # 修改名称
    @pytest.mark.smoke
    def _change_name_of_mongo_instance(self,config, instance_data, http_client, create_mongo_instance):
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
	info_logger.info("[VERIFICATION] The name changed is the same with the specific name")
	assert name_changed == mongo_info["name"], "[ERROR] It is failed to change name for the mongo instance {0}".format(space_id)

    # 创建mongo实例，验证实际mongo对应的container的副本集关系与创建时设置的副本集关系一致 
    def _create_mongo_instance_and_verify_replica(self, config, instance_data, http_client, mysql_client, docker_client, create_mongo_instance):
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

    #通过flavor信息，查看数据库flavor表中flavor id；在根据flavor id查看数据库flavor中的信息
    @pytest.mark.smoke
    def _flavor_info(self, config, instance_data, http_client):
	# info_logger.info("[SCENARIO] Verify flavor info is the same with flavor id")
        # 获取flavor 1C_2M_4D_10E的flavor id
        info_logger.info("[STEP] Get flavor id by flavor info")
        flavor_id = get_flavorid_by_flavorinfo_step(instance_data, http_client)
        info_logger.info("[INFO] Flavor id is %s for flavor info [%s]", flavor_id, instance_data["mongo_1C_2M_4D_10E"])
        assert flavor_id != "", "[ERROR] Flavor id is none"
	# 根据flavor id获取flavor info的信息与stpe1的flavor信息一致
	flavor_info = get_flavor_info_step(instance_data, http_client, flavor_id)
	info_logger.info("[INFO] Flavor info is %s", json.dumps(flavor_info))
	assert flavor_info["cpu"] == int(instance_data["mongo_1C_2M_4D_10E"]["cpu"]), "[ERROR] CPU is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["cpu"]))
	assert flavor_info["disk"] == int(instance_data["mongo_1C_2M_4D_10E"]["disk"]), "[ERROR] Disk is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["disk"]))
	assert flavor_info["memory"] == int(instance_data["mongo_1C_2M_4D_10E"]["memory"]), "[ERROR] Memory is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["memory"]))
	assert flavor_info["iops"] == int(instance_data["mongo_1C_2M_4D_10E"]["iops"]), "[ERROR] Iops is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["iops"]))
	assert flavor_info["maxConn"] == int(instance_data["mongo_1C_2M_4D_10E"]["maxconn"]), "[ERROR] Iops is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["maxConn"]))

    #删除mongo实例
    def _delete_mongo_instance(self, config, instance_data, http_client, mysql_client, docker_client):
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
	info_logger.info("[INFO] The status of the container {} is aliv", container_1["docker_id"])
	# 删除mongo实例
	info_logger.info("[STEP] Delete the mongo instance %s", space_id)
        delete_instance_step(config, instance_data, http_client, space_id)
	time.sleep(int(instance_data["wait_time"]))
	status_for_delete_instance = get_status_of_deleted_instance_step(config, instance_data, http_client, space_id)
	assert 102 == status_for_delete_instance, "[ERROR] The mongo instance [{0}] cannot be deleted".format(space_id)
	# 验证通过物理资源机查看mongo实例对应的container已经不存在
	is_alive =  ping_container_step(config, instance_data, http_client, docker_client, container_1)
	assert "false" == is_alive, "[ERROR] The container [{0}] is not alive or not exited".format(container_1["docker_id"])
