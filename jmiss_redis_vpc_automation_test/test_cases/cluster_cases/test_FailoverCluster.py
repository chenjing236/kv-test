# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestFailoverCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_master(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password = created_instance
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_cfs_step(cluster)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["masterDocker"], container, cfs_client, 2)
        assert is_failover is True, info_logger.error("Run master failover is failed")
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        assert shards[failover_num]["masterDocker"] != shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] == shards_cfs[failover_num]["slaveDocker"]
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_slave(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password = created_instance
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # run slave failover
        cfs_host = get_master_cfs_step(cluster)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("To stop the slave container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["slaveDocker"], container, cfs_client, 1)
        assert is_failover is True, info_logger.error("Run slave failover is failed")
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        assert shards[failover_num]["masterDocker"] == shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] != shards_cfs[failover_num]["slaveDocker"]
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
