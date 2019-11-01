# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestFailoverInstance:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_ms_redis_master_stop_docker(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 获取当前拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_server_step(instance, "cfs")
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
    def test_failover_ms_redis_slave_stop_docker(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 获取当前拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # run slave failover
        cfs_host = get_master_server_step(instance, "cfs")
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, slaveDocker, container, cfs_client, 1)
        assert is_failover is True, info_logger.error("Run master failover is failed")
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        assert masterDocker == masterPort_cfs
        assert slaveDocker != slavePort_cfs
        # 通过domain访问缓存云实例，执行set/get key
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_ms_proxy(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 获取当前proxy列表
        proxy_list = get_proxy_list_of_instance_step(instance, space_id)
        assert len(proxy_list) != 0
        proxy_docker = proxy_list[0]["dockerId"]
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # run proxy failover
        cfs_host = get_master_server_step(instance, "cfs")
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, proxy_docker, container, cfs_client, 1)
        assert is_failover is True, info_logger.error("Run proxy failover is failed")
        proxy_list_new = get_proxy_list_of_instance_step(instance, space_id)
        proxy_docker_new = proxy_list_new[0]["dockerId"]
        assert proxy_docker != proxy_docker_new
        # 通过domain访问缓存云实例，执行set/get key
        # check_access_domain_step(accesser, space_id, password)
