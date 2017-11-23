# coding:utf-8
from BasicTestCase import *
import json

info_logger = logging.getLogger(__name__)


class TestCreateCluster:
    @pytest.mark.createcluster
    def test_create_cluster_with_db(self, config, instance_data, http_client, sql_client):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        cluster = Cluster(config, instance_data, http_client)
        # 调用创建缓存云集群接口，创建缓存云集群
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, password = create_instance_with_password_step(cluster)
        self.space_id = space_id
        # 调用查询接口等待缓存云集群创建完成
        info_logger.info("The cluster %s is created", space_id)
        info_logger.info("[STEP2] Get detailed information of the cluster %s", space_id)
        status, capacity = get_status_of_instance_step(cluster, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        info_logger.info("Status of the cluster %s is %s", space_id, status)
        assert status == 100
        # 查询数据库space表，验证缓存云实例状态status=100
        info_logger.info("[STEP3] Check space info in db of the cluster %s", space_id)
        space = sql_client.get_space_status(space_id)
        if space is None:
            info_logger.error("get space:[{0}] status from db failed!".format(space_id))
            return 1
        status, capacity, password, cluster_type, tenant_id, name, remarks = space
        assert status == 100
        # 删除缓存云实例
        info_logger.info("[STEP4] Delete the cluster %s", space_id)
        delete_instance_step(cluster, space_id)

    @pytest.mark.createcluster
    def test_topology_with_db(self, config, instance_data, created_instance, sql_client):
        # 创建缓存云集群
        info_logger.info("Create a cluster with a set of master and slave containers")
        space_id, cluster = created_instance
        info_logger.info("The cluster %s is created", space_id)
        # 查看CFS中的redis拓扑结构
        info_logger.info("Get topology of cluster [{0}] from CFS".format(space_id))
        capa = instance_data['capacity']
        cfs_client = CFS(config, capa)
        topology_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        print "topology_cfs = ", topology_cfs
        # 查看数据库topology表中的拓扑结构
        info_logger.info("Get current topology of cluster [{0}] from db".format(space_id))
        capacity = instance_data['capacity']
        shard_count = config['cluster_cfg'][str(int(capacity) / 1024 / 1024)]
        current_topology = sql_client.get_current_topology(space_id)
        if current_topology is None:
            info_logger.error("get cluster [{0}] topology from db failed!".format(space_id))
            return 1
        print current_topology
        print json.dumps(current_topology)
        print json.loads(current_topology)
        topology_db = change_topology_json_to_list(shard_count, json.loads(current_topology))
        print "topology_db = ", topology_db
        # 查看数据库instance表中的拓扑结构
        info_logger.info("Get instance info of cluster [{0}] from db".format(space_id))
        topology_ins = sql_client.get_instances_of_cluster(space_id, shard_count)
        if topology_ins is None or len(topology_ins) != shard_count:
            info_logger.error("Get instance info of cluster from db failed!")
            return 1
        print "topology_ins = ", topology_ins
        # 验证拓扑结构的一致性
        assert topology_ins == topology_cfs
        info_logger.info("Topology from table instance is same as topology from CFS")
        assert topology_db == topology_ins
        info_logger.info("Topology from table topology is same as topology from table instance!")
        info_logger.info("It's successful to check topology of cluster!")

    # @pytest.mark.createcluster
    # def test_container_info_with_db(self, config, instance_data, created_instance, sql_client):
    #     # 创建缓存云集群
    #     info_logger.info("Create a cluster with a set of master and slave containers")
    #     space_id, cluster = created_instance
    #     info_logger.info("The cluster %s is created", space_id)
    #     # 查看CFS中的redis拓扑结构
    #     info_logger.info("Get topology of cluster [{0}] from CFS".format(space_id))
    #     capa = instance_data['capacity']
    #     cfs_client = CFS(config, capa)
    #     topology_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
    #     print "topology_cfs = ", topology_cfs

    @pytest.mark.createcluster
    def test_create_cluster(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        cluster = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id = create_instance_step(cluster)
        info_logger.info("The cluster %s is created", space_id)
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the cluster %s", space_id)
        status, capacity = get_status_of_instance_step(cluster, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        info_logger.info("Status of the cluster %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP3] Get topology information of cluster")
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 获取CFS的拓扑结构
        info_logger.info("[STEP4] Get topology information of cluster from CFS")
        capa = instance_data['capacity']
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config, capa)
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards_cfs[i]))
        for i in range(0, shard_count):
            assert shards[i]["masterIp"] == shards_cfs[i]["masterIp"]
            assert shards[i]["masterPort"] == shards_cfs[i]["masterPort"]
            assert shards[i]["slaveIp"] == shards_cfs[i]["slaveIp"]
            assert shards[i]["slavePort"] == shards_cfs[i]["slavePort"]
        # 获取container的大小，验证container的大小
        container = Container(config)
        for i in range(0, shard_count):
            master_memory_size, slave_memory_size = get_container_memory_size_step(container, shards[i]["masterIp"], shards[i]["masterPort"], shards[i]["slaveIp"], shards[i]["slavePort"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, master_memory_size))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, slave_memory_size))
            assert master_memory_size == capacity / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert slave_memory_size == capacity / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        info_logger.info("[STEP5] Delete the cluster %s", space_id)
        delete_instance_step(cluster, space_id)

    @pytest.mark.createcluster
    def test_create_cluster_with_password(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        cluster = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        password = "password"
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id = create_instance_with_password_step(cluster, password)
        info_logger.info("The cluster %s is created", space_id)
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the cluster %s", space_id)
        status, capacity = get_status_of_instance_step(cluster, space_id, int(config["retry_getting_info_times"]),
                                                       int(config["wait_time"]))
        info_logger.info("Status of the cluster %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP3] Get topology information of cluster")
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 获取CFS的拓扑结构
        info_logger.info("[STEP4] Get topology information of cluster from CFS")
        capa = instance_data['capacity']
        cfs_client = CFS(config, capa)
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards_cfs[i]))
        for i in range(0, shard_count):
            assert shards[i]["masterIp"] == shards_cfs[i]["masterIp"]
            assert shards[i]["masterPort"] == shards_cfs[i]["masterPort"]
            assert shards[i]["slaveIp"] == shards_cfs[i]["slaveIp"]
            assert shards[i]["slavePort"] == shards_cfs[i]["slavePort"]
        # 获取container的大小，验证container的大小
        container = Container(config)
        for i in range(0, shard_count):
            master_memory_size, slave_memory_size = get_container_memory_size_step(container, shards[i]["masterIp"],
                                                                              shards[i]["masterPort"],
                                                                              shards[i]["slaveIp"],
                                                                              shards[i]["slavePort"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, master_memory_size))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, slave_memory_size))
            assert master_memory_size == capacity / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert slave_memory_size == capacity / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        info_logger.info("[STEP5] Delete the cluster %s", space_id)
        delete_instance_step(cluster, space_id)
