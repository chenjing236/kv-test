# coding:utf-8
from BasicTestCase import *
import json

info_logger = logging.getLogger(__name__)


class TestCreateCluster:
    @pytest.mark.createcluster
    def test_create_cluster(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create a cluster with a set of master and slave containers")
        cluster = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, operation_id, password = create_instance_step(cluster)
        info_logger.info("[INFO] The cluster {0} is created, its password is {1}".format(space_id, password))
        # 查看创建操作结果，验证创建成功
        info_logger.info("[STEP2] Get creation result of the cluster {0}".format(space_id))
        is_success = get_operation_result_step(cluster, space_id, operation_id)
        assert is_success is True, "[INFO] Get the right operation result, create cluster successfully"
        # 设置资源acl
        info_logger.info("[STEP3] Set enable acl for the instance {0}".format(space_id))
        set_acl_step(cluster, space_id)
        info_logger.info("[INFO] Set acl successfully!")
        # 查看缓存云实例详细信息
        info_logger.info("[STEP4] Get detail info of the instance {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        assert detail_info["status"] == 100, "[ERROR] The cluster status is not 100!"
        assert detail_info["zone"] != 'clsdocker', "[ERROR] The cluster zone is clsdocker!"
        info_logger.info("[INFO] Get the right detail info, the status of cluster {0} is 100".format(space_id))
        capacity = detail_info["capacity"]
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP5] Get topology information of cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 获取CFS的拓扑结构
        info_logger.info("[STEP6] Get topology information of cluster from CFS")
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards_cfs[i]))
        for i in range(0, shard_count):
            assert shards[i]["masterIp"] == shards_cfs[i]["masterIp"]
            assert shards[i]["masterDocker"] == shards_cfs[i]["masterDocker"]
            assert shards[i]["slaveIp"] == shards_cfs[i]["slaveIp"]
            assert shards[i]["slaveDocker"] == shards_cfs[i]["slaveDocker"]
        # 获取container的大小，验证container的大小
        info_logger.info("[STEP7] Get container info from nova agent")
        container = Container(config, http_client)
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave))
            assert mem_info_master["total"] == capacity * 1024 / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert mem_info_slave["total"] == capacity * 1024 / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        info_logger.info("[STEP8] Delete the instance {0}".format(space_id))
        delete_instance_step(cluster, space_id)
        # 删除较慢，加等待时间，防止资源不够创建失败
        time.sleep(15)
