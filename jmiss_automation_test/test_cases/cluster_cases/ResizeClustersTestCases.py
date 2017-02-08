# coding:utf-8
from BasicTestCase import *
import json

info_logger = logging.getLogger(__name__)


class TestResizeCluster:
    # @pytest.mark.resizecluster
    # def test_resize_cluster_with_db(self, config, instance_data, http_client, sql_client):
    #     info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
    #     cluster = Cluster(config, instance_data, http_client)
    #     # 调用创建缓存云集群接口，创建缓存云集群
    #     info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
    #     space_id = create_instance_step(cluster)
    #     self.space_id = space_id
    #     # 调用查询接口等待缓存云集群创建完成
    #     info_logger.info("The cluster %s is created", space_id)
    #     info_logger.info("[STEP2] Get detailed information of the cluster %s", space_id)
    #     status, capacity = get_status_of_instance_step(cluster, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
    #     info_logger.info("Status of the cluster %s is %s", space_id, status)
    #     assert status == 100
    #     # 查询数据库space表，验证缓存云实例状态status=100
    #     info_logger.info("[STEP3] Check space info in db of the cluster %s", space_id)
    #     space = sql_client.get_space_status(space_id)
    #     if space is None:
    #         info_logger.error("get space:[{0}] status from db failed!".format(space_id))
    #         return 1
    #     status, capacity, password, cluster_type, tenant_id, name, remarks = space
    #     assert status == 100
    #     # 删除缓存云实例
    #     info_logger.info("[STEP4] Delete the cluster %s", space_id)
    #     delete_instance_step(cluster, space_id)

    @pytest.mark.resizecluster
    def test_resize_cluster(self, config, instance_data,  created_instance):
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
