# coding:utf-8
from BasicTestCase import *


class TestResizeInstance:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_resize_instance_to_instance(self, config, instance_data, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 获取原有缓存云实例的flavor
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)
        # 执行扩容操作
        flavor_id_resize = instance_data["flavorIdResize"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, info_logger.error("The flavor is incorrect after resizing the instance {0}".format(space_id))
        assert flavor_id_new == flavor_id_resize, info_logger.error("The flavor is incorrect after resizing the instance {0}".format(space_id))
        assert status == 100, info_logger.error("The status of instance [{0}] is not 100!".format(space_id))
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024*1024*1024 if capacity < 16*1024*1024*1024 else 2*1024*1024*1024
        # mem_total和capacity单位均为byte
        assert mem_info_master["mem_total"] == capacity + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
        assert mem_info_slave["mem_total"] == capacity + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.regression
    def test_reduce_instance_to_instance(self, config, instance_data, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 获取原有缓存云实例的flavor
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)
        # 执行缩容操作
        flavor_id_reduce = instance_data["flavorIdReduce"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_reduce)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, info_logger.error("The flavor is incorrect after reducing the instance {0}".format(space_id))
        assert flavor_id_new == flavor_id_reduce, info_logger.error("The flavor is incorrect after reducing the instance {0}".format(space_id))
        assert status == 100, info_logger.error("The status of instance [{0}] is not 100!".format(space_id))
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024*1024*1024 if capacity < 16*1024*1024*1024 else 2*1024*1024*1024
        # mem_total和capacity单位均为byte
        assert mem_info_master["mem_total"] == capacity + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
        assert mem_info_slave["mem_total"] == capacity + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_resize_instance_to_cluster(self, config, instance_data, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 获取原有缓存云实例的flavor
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)
        # 执行扩容操作
        flavor_id_resize = instance_data["flavorIdResizeToCluster"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, info_logger.error("The flavor is incorrect after resizing the instance {0}".format(space_id))
        assert flavor_id_new == flavor_id_resize, info_logger.error("The flavor is incorrect after resizing the instance {0}".format(space_id))
        assert status == 100, info_logger.error("The status of instance [{0}] is not 100!".format(space_id))
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取扩容后集群的拓扑结构
        shards = get_topology_of_cluster_step(instance, space_id)
        shard_count = len(shards)
        container = Container(config, http_client)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024 * 1024 * 1024 if capacity / shard_count < 16 * 1024 * 1024 * 1024 else 2 * 1024 * 1024 * 1024
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master["mem_total"]))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave["mem_total"]))
            assert mem_info_master["mem_total"] == capacity / shard_count + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
            assert mem_info_slave["mem_total"] == capacity / shard_count + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # 验证通过nlb访问实例
        check_access_domain_step(accesser, space_id, password)
