# coding:utf-8
import pytest
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesOfCluster:

    @pytest.mark.smoke
    def test_create_cluster(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        cluster = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id = create_instance_step(cluster)
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


    @pytest.mark.smoke
    def test_access_ap(self, config, created_instance):
        info_logger.info("[SCENARIO] It is successful to access AP and to set/get key")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster = created_instance
        info_logger.info("The cluster %s is created", space_id)
        # 获取AP的token
        info_logger.info("[STEP2] Get token for the status %s", space_id)
        instance_info = get_detail_info_of_instance_step(cluster, space_id)
        password = instance_info["password"]
        # domain = instance_info["domain"]
        info_logger.info("Token is %s for the cluster %s", password, space_id)
        # 获取拓扑结构
        info_logger.info("Get topology information of the cluster %s", space_id)
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the cluster %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)

    @pytest.mark.smoke
    def test_resize_cluster(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster = created_instance
        info_logger.info("The cluster %s is created", space_id)
        # 获取原有缓存云实例的capacity
        info_logger.info("[STEP2] Get the token of the origin cluster %s", space_id)
        instance_info = get_detail_info_of_instance_step(cluster, space_id)
        capacity_origin = int(instance_info["capacity"])
        password = instance_info["password"]
        info_logger.info("The token of the cluster %s is %s", space_id, password)
        # 获取拓扑结构
        info_logger.info("[STEP3] Get topology information of the cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the cluster {0}".format(space_id))
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP")
        # 通过ap set key-value
        key, value = set_key_from_ap_step(config["ap_host"], config["ap_port"], password, "test_key", "test_value")
        # assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to set the value by key from the cluster %s", space_id)
        # 执行扩容操作
        info_logger.info("[STEP6] Resize the cluster %s", space_id)
        cfs_client = CFS(config)
        zoneId = int(instance_data["zoneId"])
        capacity = int(instance_data["capacity_resize"])
        status, capacity_new = resize_instance_step(cluster, cfs_client, space_id, zoneId, capacity,
                                                    config["retry_times"], int(config["wait_time"]))
        # 验证扩容操作后的大小
        assert capacity_new != capacity_origin, "[ERROR] The capacity is incorrect after resizing the cluster {0}".format(
            space_id)
        assert capacity_new == capacity, "[ERROR] The capacity is incorrect after resizing the cluster {0}".format(
            space_id)
        info_logger.info("[INFO] It is successful to resize the cluster %s", space_id)
        # 通过AP访问获取key
        info_logger.info("[STEP6] Get key from the instance reiszed %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instanche {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get value from the instance %s", space_id)

    @pytest.mark.smoke
    def test_failover(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] It is successful to run failover master of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster = created_instance
        info_logger.info("The cluster %s is created", space_id)
        # 获取原有缓存云实例的capacity
        info_logger.info("[STEP2] Get the token of the origin cluster %s", space_id)
        instance_info = get_detail_info_of_instance_step(cluster, space_id)
        password = instance_info["password"]
        info_logger.info("The token of the cluster %s is %s", space_id, password)
        # 获取拓扑结构
        info_logger.info("[STEP3] Get topology information of the cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the cluster {0}".format(space_id))
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
        # run master failover
        info_logger.info("[STEP6] Run failover for master container")
        capa = instance_data['capacity']
        cfs_client = CFS(config, capa)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover, master_ip_new, master_port_new, slave_ip_new, slave_port_new = run_failover_container_of_cluster_step(
            cluster, cfs_client, container, space_id, 2, shards[failover_num]["masterIp"],
            shards[failover_num]["masterPort"], retry_times, wait_time)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        info_logger.info("Information of master container is %s:%s", master_ip_new, master_port_new)
        info_logger.info("Information of slave container is %s:%s", slave_ip_new, slave_port_new)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
