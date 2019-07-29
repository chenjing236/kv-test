# coding:utf-8
from BasicTestCase import *


class TestFailoverCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_master(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_cfs_step(instance)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, masterDocker, container, cfs_client, 2)
        assert is_failover is True, info_logger.error("Run master failover is failed")
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        assert masterDocker != masterPort_cfs
        assert slaveDocker == slavePort_cfs
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_slave(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)
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
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_ap(self, config, created_instance, http_client, sql_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)
        container = Container(config, http_client)
        # 执行ap failover
        run_ap_failover_step(container, space_id, sql_client)
        # 验证数据库中topology version与ap内存中一致
        check_topology_verison_of_ap_step(container, sql_client, space_id)
        check_access_domain_step(accesser, space_id, password)
