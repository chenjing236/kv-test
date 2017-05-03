# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestCreateInstance:
    # 创建单实例缓存云实例，并验证数据库中的数据
    # @pytest.mark.smoke
    # def test_create_an_instance_using_db(self, config, instance_data, http_client):
    #     info_logger.info("[Scenario] It is successful to create an instance whith a master container and a slave container")
    #     # 调用创建缓存云实例接口，创建单实例缓存云
    #     info_logger.info("[STEP1] Create an instance including a master container and a slave container")
    #     instance = Cluster(config, instance_data, http_client)
    #     # 查询数据库表space表，查看缓存云实例的状态status=100
    #     space_id = create_instance_step(instance)
    #
    # @pytest.mark.smoke
    # def F_test_topology_info_using_db(self):
    #     print "[Scenario] The information of topology for the instance is correct"
    #     info_logger.info("[Scenario] The information of topology for the instance is correct")
    #     # 查看数据库topology表中拓扑结构
    #     # 查看数据库instance表中拓扑结构
    #     # 查看CFS的redis中的信息
    #
    # @pytest.mark.smoke
    # def F_test_container_info(self):
    #     print "[Scenario] The information of containers for the instance is correct"
    #     info_logger.info("[Scenario] The information of containers for the instance is correct")
    #     # 查看container信息，master continer是否是运行状态，且replication是master
    #     # 查看container信息，master continer的大小
    #     # 查看container信息，slave container是否是运行状态，且replication是slave
    #     # 查看container信息，slave continer的大小

    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.createInstance
    def test_create_instance_with_password(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        space_id, password = create_instance_with_password_step(instance, instance_data["password"])
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the instance %s", space_id)
        status, capacity = get_status_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]),
                                                       int(config["wait_time"]))
        info_logger.info("[INFO] Status of the instance %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP3] Get topology information of instance")
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        # 获取CFS的拓扑结构
        info_logger.info("[STEP4] Get topology information of instance from CFS")
        cfs_client = CFS(config)
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client,
                                                                                                          space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp_cfs, masterPort_cfs)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_cfs, slavePort_cfs)
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterPort == masterPort_cfs, "[ERROR] Port of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slavePort == slavePort_cfs, "[ERROR] Port of slave container is inconsistent"
        # 获取container的大小，验证container的大小
        container = Container(config)
        master_memory_size, slave_memory_size = get_container_memory_size_step(container, masterIp, masterPort, slaveIp,
                                                                               slavePort)
        info_logger.info("[INFO] Memory size of master container is %s", master_memory_size)
        assert master_memory_size == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert slave_memory_size == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        info_logger.info("[STEP5] Delete the instance %s", space_id)
        delete_instance_step(instance, space_id)
        # assert False, "[ERROR] test error log"
