# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestFailoverCluster:
    @pytest.mark.smoke
    def test_failover_master(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] It is successful to run failover master of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # run master failover
        cfs_client = CFS(config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["masterDocker"], container, cfs_client, 2)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        logger_info.info("[INFO] It is successful to run master failover")
        info_logger.info("[STEP4] Get topology information from CFS {0}".format(space_id))
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Master container of shard_{0} after master failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["masterIp"], shards_cfs[failover_num]["masterDocker"]))
        info_logger.info("[INFO] Slave container of shard_{0} after master failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["slaveIp"], shards_cfs[failover_num]["slaveDocker"]))
        assert shards[failover_num]["masterDocker"] != shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] == shards_cfs[failover_num]["slaveDocker"]
        info_logger.info("[INFO] Test master failover successfully!")

    @pytest.mark.smoke
    def test_failover_slave(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] It is successful to run failover slave of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of slave container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # run master failover
        cfs_client = CFS(config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the slave container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["slaveDocker"], container, cfs_client, 1)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        logger_info.info("[INFO] It is successful to run slave failover")
        info_logger.info("[STEP4] Get topology information from CFS {0}".format(space_id))
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Master container of shard_{0} after slave failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["masterIp"], shards_cfs[failover_num]["masterDocker"]))
        info_logger.info("[INFO] Slave container of shard_{0} after slave failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["slaveIp"], shards_cfs[failover_num]["slaveDocker"]))
        assert shards[failover_num]["masterDocker"] == shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] != shards_cfs[failover_num]["slaveDocker"]
        info_logger.info("[INFO] Test slave failover successfully!")
