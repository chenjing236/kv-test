# coding:utf-8
from BasicTestCase import *


class TestCreateInstance:
    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_instance(self, config, created_instance, http_client):
        # 创建缓存云实例
        space_id, instance, password = created_instance
        # 查看redis详情，验证缓存云实例状态，status=100创建成功
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        capacity = detail_info["capacity"]
        # 查看缓存云实例详情，获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 获取CFS的拓扑结构
        cfs_host = get_master_cfs_step(instance)
        cfs_client = CFS(cfs_host, config)
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        assert masterIp == masterIp_cfs, info_logger.error("Ip of master container is inconsistent")
        assert masterDocker == masterDocker_cfs, info_logger.error("Docker_id of master container is inconsistent")
        assert slaveIp == slaveIp_cfs, info_logger.error("Ip of slave container is inconsistent")
        assert slaveDocker == slaveDocker_cfs, info_logger.error("Docker_id of slave container is inconsistent")
        # 获取container的大小，验证container的大小
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master["total"] == capacity * 1024, info_logger.error("Memory size of master container is inconsistent with request")
        assert mem_info_slave["total"] == capacity * 1024, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
