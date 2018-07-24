# coding:utf-8
from BasicTestCase import *


# todo：ap failover
class TestFailoverCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_master(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password = created_instance
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 通过AP访问缓存云实例，执行set/get key
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_cfs_step(instance)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, masterDocker, container, cfs_client, 2)
        assert is_failover is True, info_logger.error("Run master failover is failed")
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        assert masterDocker != masterPort_cfs
        assert slaveDocker == slavePort_cfs
        # 通过AP访问缓存云实例，执行set/get key
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_slave(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password = created_instance
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 通过AP访问缓存云实例，执行set/get key
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_cfs_step(instance)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, slaveDocker, container, cfs_client, 1)
        assert is_failover is True, info_logger.error("Run slave failover is failed")
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(
            cfs_client, space_id)
        assert masterDocker == masterDocker_cfs
        assert slaveDocker != slaveDocker_cfs
        # 通过AP访问缓存云实例，执行set/get key
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
