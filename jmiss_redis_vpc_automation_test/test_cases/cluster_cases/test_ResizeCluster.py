# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResizeCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_resize_cluster(self, config, instance_data, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password = created_instance
        # 获取原有缓存云实例的capacity
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        flavor_id = detail_info["flavorId"]
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # 执行扩容操作
        flavor_id_resize = instance_data["flavorIdResize"]
        status, flavor_id_new = resize_instance_step(cluster, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, info_logger.error("The flavor is incorrect after resizing the cluster {0}".format(space_id))
        assert flavor_id_new == flavor_id_resize, info_logger.error("The flavor is incorrect after resizing the cluster {0}".format(space_id))
        assert status == 100, info_logger.error("The status of cluster [{0}] is not 100!".format(space_id))
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(cluster, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        container = Container(config, http_client)
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave))
            assert mem_info_master["total"] == capacity / shard_count, info_logger.error("Memory size of master container is inconsistent with request")
            assert mem_info_slave["total"] == capacity / shard_count, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_reduce_cluster(self, config, instance_data, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password = created_instance
        # 获取原有缓存云实例的capacity
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        flavor_id = detail_info["flavorId"]
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # 执行缩容操作
        flavor_id_reduce = instance_data["flavorIdReduce"]
        status, flavor_id_new = resize_instance_step(cluster, space_id, flavor_id_reduce)
        # 验证缩容操作后的规格
        assert flavor_id_new != flavor_id, info_logger.error("The flavor is incorrect after reducing the cluster {0}".format(space_id))
        assert flavor_id_new == flavor_id_reduce, info_logger.error("The flavor is incorrect after reducing the cluster {0}".format(space_id))
        assert status == 100, info_logger.error("The status of cluster [{0}] is not 100!".format(space_id))
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(cluster, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        container = Container(config, http_client)
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave))
            assert mem_info_master["total"] == capacity / shard_count, info_logger.error("Memory size of master container is inconsistent with request")
            assert mem_info_slave["total"] == capacity / shard_count, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
