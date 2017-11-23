# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestFailoverCluster:
    @pytest.mark.smoke
    def test_failover_master(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] It is successful to run failover master of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster %s is created", space_id)
        info_logger.info("[INFO] The password of the cluster %s is %s", space_id, password)
        # 获取原有缓存云实例的capacity
        # info_logger.info("[STEP2] Get the token of the origin cluster %s", space_id)
        # instance_info = get_detail_info_of_instance_step(cluster, space_id)
        # password = instance_info["password"]
        # info_logger.info("The token of the cluster %s is %s", space_id, password)
        # 获取拓扑结构
        info_logger.info("[STEP3] Get topology information of the cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("[INFO] Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the cluster {0}".format(space_id))
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key from the cluster %s", space_id)
        # run master failover
        info_logger.info("[STEP6] Run failover for master container")
        capa = instance_data['capacity']
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config, capa)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover, master_ip_new, master_port_new, slave_ip_new, slave_port_new = run_failover_container_of_cluster_step(
            cluster, cfs_client, container, space_id, 2, shards[failover_num]["masterIp"],
            shards[failover_num]["masterPort"], retry_times, wait_time)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        info_logger.info("[INFO] Information of master container is %s:%s", master_ip_new, master_port_new)
        info_logger.info("[INFO] Information of slave container is %s:%s", slave_ip_new, slave_port_new)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key from the cluster %s", space_id)

    @pytest.mark.smoke
    def test_failover_slave(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] It is successful to run failover slave of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster %s is created", space_id)
        info_logger.info("[INFO] The password of the cluster %s is %s", space_id, password)
        # 获取原有缓存云实例的capacity
        # info_logger.info("[STEP2] Get the token of the origin cluster %s", space_id)
        # instance_info = get_detail_info_of_instance_step(cluster, space_id)
        # password = instance_info["password"]
        # info_logger.info("The token of the cluster %s is %s", space_id, password)
        # 获取拓扑结构
        info_logger.info("[STEP3] Get topology information of the cluster %s", space_id)
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        for i in range(0, shard_count):
            info_logger.info("[INFO] Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the cluster %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key from the cluster %s", space_id)
        # run master failover
        info_logger.info("[STEP6] Run failover for master container")
        capa = instance_data['capacity']
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config, capa)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover, master_ip_new, master_port_new, slave_ip_new, slave_port_new = run_failover_container_of_cluster_step(
            cluster, cfs_client, container, space_id, 1, shards[failover_num]["slaveIp"],
            shards[failover_num]["slavePort"], retry_times, wait_time)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        info_logger.info("[INFO] Information of slave container is %s:%s", master_ip_new, master_port_new)
        info_logger.info("[INFO] Information of slave container is %s:%s", slave_ip_new, slave_port_new)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key from the cluster %s", space_id)
