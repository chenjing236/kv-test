# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResizeCluster:

    @pytest.mark.resizecluster
    def test_resize_cluster(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to resize a cluster")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的capacity
        info_logger.info("[STEP2] Get the flavor of the origin cluster {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin cluster is [{0}]".format(flavor_id))
        # 执行扩容操作
        info_logger.info("[STEP3] Resize the cluster {0}".format(space_id))
        flavor_id_resize = instance_data["flavorIdResize"]
        status, flavor_id_new = resize_instance_step(cluster, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after resizing the cluster {0}"\
            .format(space_id)
        assert flavor_id_new == flavor_id_resize, "[ERROR] The flavor is incorrect after resizing the cluster {0}"\
            .format(space_id)
        assert status == 100, "[ERROR] The status of cluster [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(cluster, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of cluster {0} after resize".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        info_logger.info("[STEP5] Check the capacity of cluster after resize")
        container = Container(config, http_client)
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave))
            assert mem_info_master["total"] == capacity / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert mem_info_slave["total"] == capacity / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to resize the cluster [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))

    @pytest.mark.resizecluster
    def test_reduce_cluster(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to reduce a cluster")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的capacity
        info_logger.info("[STEP2] Get the flavor of the origin cluster {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin cluster is [{0}]".format(flavor_id))
        # 执行缩容操作
        info_logger.info("[STEP3] Reduce the cluster {0}".format(space_id))
        flavor_id_reduce = instance_data["flavorIdReduce"]
        status, flavor_id_new = resize_instance_step(cluster, space_id, flavor_id_reduce)
        # 验证缩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after reducing the cluster {0}" \
            .format(space_id)
        assert flavor_id_new == flavor_id_reduce, "[ERROR] The flavor is incorrect after reducing the cluster {0}" \
            .format(space_id)
        assert status == 100, "[ERROR] The status of cluster [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(cluster, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of cluster {0} after reduce".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        info_logger.info("[STEP5] Check the capacity of cluster after reduce")
        container = Container(config, http_client)
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave))
            assert mem_info_master["total"] == capacity / shard_count, "[ERROR] Memory size of master container is inconsistent with request"
            assert mem_info_slave["total"] == capacity / shard_count, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to reduce the cluster [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))
