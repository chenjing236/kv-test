# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestResizeInstance:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_resize_ms_to_larger_ms(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceClass"] != instance_data["cache_instance_class_resize"]
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # 执行扩容操作
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceStatus"] == "running"
        assert cluster_detail_new["cacheInstanceClass"] == instance_data["cache_instance_class_resize"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        capacity = cluster_detail_new["cacheInstanceMemoryMB"]
        # 查看缓存云实例详情，获取拓扑结构
        instance = Cluster(config, instance_data, http_client)
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 获取container的大小，验证container的大小
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024*1024*1024 if capacity < 16*1024 else 2*1024*1024*1024
        # mem_total单位为byte，capacity单位为MB
        assert mem_info_master["mem_total"] == capacity * 1024 * 1024 + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
        assert mem_info_slave["mem_total"] == capacity * 1024 * 1024 + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # # 验证数据库中topology version与ap内存中一致
        # check_topology_verison_of_ap_step(container, sql_client, space_id)

        # # 验证通过nlb访问实例
        # accesser = Accesser(config)
        # ping_domain_step(accesser, space_id)
        # check_access_domain_step(accesser, space_id, password)

    @pytest.mark.regression
    def test_resize_ms_to_smaller_ms(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceClass"] != instance_data["cache_instance_class_reduce"]
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # 执行缩容操作
        cache_instance_class_reduce = instance_data["cache_instance_class_reduce"]
        error = resize_step(redis_cap, space_id, cache_instance_class_reduce)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceStatus"] == "running"
        assert cluster_detail_new["cacheInstanceClass"] == instance_data["cache_instance_class_reduce"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        capacity = cluster_detail_new["cacheInstanceMemoryMB"]
        # 通过jmiss-web查看缓存云实例详情，获取拓扑结构
        instance = Cluster(config, instance_data, http_client)
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 获取container的大小，验证container的大小
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024 * 1024 * 1024 if capacity < 16 * 1024 else 2 * 1024 * 1024 * 1024
        # mem_total单位为byte，capacity单位为MB
        assert mem_info_master["mem_total"] == capacity * 1024 * 1024 + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
        assert mem_info_slave["mem_total"] == capacity * 1024 * 1024 + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # # 验证数据库中topology version与ap内存中一致
        # check_topology_verison_of_ap_step(container, sql_client, space_id)

        # # 验证通过nlb访问实例
        # accesser = Accesser(config)
        # ping_domain_step(accesser, space_id)
        # check_access_domain_step(accesser, space_id, password)

    # todo: resize_cluster_to_larger_cluster
    # todo: resize_cluster_to_smaller_cluster

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_resize_ms_to_cluster(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceClass"] != instance_data["cache_cluster_class"]
        assert cluster_detail["cacheInstanceType"] == "master-slave"
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # 执行扩容操作
        cache_cluster_class = instance_data["cache_cluster_class"]
        error = resize_step(redis_cap, space_id, cache_cluster_class)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceStatus"] == "running"
        assert cluster_detail_new["cacheInstanceClass"] == instance_data["cache_cluster_class"]
        assert cluster_detail_new["cacheInstanceType"] == "cluster"
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        capacity = cluster_detail_new["cacheInstanceMemoryMB"]
        # 查看缓存云实例详情，获取拓扑结构
        instance = Cluster(config, instance_data, http_client)
        shards = get_topology_of_cluster_step(instance, space_id)
        shard_count = len(shards)
        # 获取container的大小，验证container的大小
        container = Container(config, http_client)
        # 资源预留内存，小于16G时预留1G，大于等于16G是预留2G
        extra_mem = 1024 * 1024 * 1024 if capacity / shard_count < 16 * 1024 else 2 * 1024 * 1024 * 1024
        for i in range(0, shard_count):
            mem_info_master = get_container_info_step(container, shards[i]["masterIp"], shards[i]["masterDocker"])
            mem_info_slave = get_container_info_step(container, shards[i]["slaveIp"], shards[i]["slaveDocker"])
            info_logger.info("Memory size of shard_{0} master container is {1}".format(i + 1, mem_info_master["mem_total"]))
            info_logger.info("Memory size of shard_{0} slave container is {1}".format(i + 1, mem_info_slave["mem_total"]))
            assert mem_info_master["mem_total"] == capacity * 1024 * 1024 / shard_count + extra_mem, info_logger.error("Memory size of master container is inconsistent with request")
            assert mem_info_slave["mem_total"] == capacity * 1024 * 1024 / shard_count + extra_mem, info_logger.error("Memory size of slave container is inconsistent with request")
        # # 验证数据库中topology version与ap内存中一致
        # check_topology_verison_of_ap_step(container, sql_client, space_id)

        # # 验证通过nlb访问实例
        # accesser = Accesser(config)
        # ping_domain_step(accesser, space_id)
        # check_access_domain_step(accesser, space_id, password)

    # todo: resize_cluster_to_ms
