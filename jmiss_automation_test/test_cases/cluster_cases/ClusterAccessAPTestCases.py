# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestAccessAP:
    @pytest.mark.accessap
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
