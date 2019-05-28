# coding:utf-8
from BasicTestCase import *
import json

info_logger = logging.getLogger(__name__)


class TestCreateCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_cluster(self, config, created_instance, http_client):
        # 创建缓存云实例
        space_id, cluster, password, accesser = created_instance
        # 查看缓存云实例详细信息
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        assert detail_info["status"] == 100, info_logger.error("The cluster status is not 100!")
        assert detail_info["zone"] != 'clsdocker', "The cluster zone is clsdocker!"
        capacity = detail_info["capacity"]
        # 查看缓存云实例详情，获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 获取CFS的拓扑结构
        cfs_host = get_master_cfs_step(cluster)
        cfs_client = CFS(cfs_host, config)
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        for i in range(0, shard_count):
            assert shards[i]["masterIp"] == shards_cfs[i]["masterIp"]
            assert shards[i]["masterDocker"] == shards_cfs[i]["masterDocker"]
            assert shards[i]["slaveIp"] == shards_cfs[i]["slaveIp"]
            assert shards[i]["slaveDocker"] == shards_cfs[i]["slaveDocker"]
        # 获取container的大小，验证container的大小
        container = Container(config, http_client)
        # 资源预留内存，小于16G时预留1G，大于等于16G时预留2G
        extra_mem = 1024 * 1024 * 1024 if capacity/shard_count < 16 * 1024 * 1024 else 2 * 1024 * 1024 * 1024
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master["mem_total"]))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave["mem_total"]))
            assert mem_info_master["mem_total"] == capacity * 1024 / shard_count + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
            assert mem_info_slave["mem_total"] == capacity * 1024 / shard_count + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)
