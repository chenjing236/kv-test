# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestCreateCluster:
    @pytest.mark.createcluster
    def test_create_an_instance(self, config, instance_data, http_client, ):
        print "\n[SCENARIO] Create a cluster with a set of master container and a slave container"
        info_logger.info("[SCENARIO] Create a cluster with a set of master container and a slave container")
        cluster = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        print "[STEP1] Create a cluster with a set of master container and a slave container"
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id = create_instance_step(cluster)
        print "[INFO] The cluster {0} is created".format(space_id)
        info_logger.info("[INFO] The cluster %s is created", space_id)
        # 查看缓存云实例详细信息
        print "[STEP2] Get detailed information of the cluster {0}".format(space_id)
        info_logger.info("[STEP2] Get detailed information of the cluster %s", space_id)
        status, capacity = get_status_of_instance_step(cluster, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        print "[INFO] Status of the cluster {0} is {1}".format(space_id, status)
        info_logger.info("[INFO] Status of the cluster %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例详情，获取拓扑结构
        print "[STEP3] Get topology information of cluster"
        info_logger.info("[STEP3] Get topology information of cluster")
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            print "[INFO] Information of shard_{0} container is {1}".format(i + 1, shards[i])
        # 获取CFS的拓扑结构
        print "[STEP4] Get topology information of cluster from CFS"
        info_logger.info("[STEP4] Get topology information of cluster from CFS")
        cfs_client = CFS(config, instance_data)
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        for i in range(0, shard_count):
            print "[INFO] Information of shard_{0} container is {1}".format(i + 1, shards_cfs[i])
        for i in range(0, shard_count):
            assert shards[i]["masterIp"] == shards_cfs[i]["masterIp"]
            assert shards[i]["masterPort"] == shards_cfs[i]["masterPort"]
            assert shards[i]["slaveIp"] == shards_cfs[i]["slaveIp"]
            assert shards[i]["slavePort"] == shards_cfs[i]["slavePort"]
        # 获取container的大小，验证container的大小
        container = Container(config)
        for i in range(0, shard_count):
            master_memory_size, slave_memory_size = get_container_memory_size(container, shards[i]["masterIp"], shards[i]["masterPort"], shards[i]["slaveIp"], shards[i]["slavePort"])
            print "[INFO] Memory size of shard_{0} master container is {1}".format(i + 1, master_memory_size)
            print "[INFO] Memory size of shard_{0} slave container is {1}".format(i + 1, slave_memory_size)
            assert master_memory_size == capacity / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert slave_memory_size == capacity / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        print "[STEP5] Delete the cluster {0}".format(space_id)
        info_logger.info("[STEP5] Delete the cluster %s", space_id)
        delete_instance_step(cluster, space_id)
