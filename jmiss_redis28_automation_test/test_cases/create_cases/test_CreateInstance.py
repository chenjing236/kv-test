# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestCreateInstance:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_ms_with_password(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["auth"] is True
        assert cluster_detail["cacheInstanceType"] == 'master-slave'
        # domain = cluster_detail["connectionDomain"]
        capacity = cluster_detail["cacheInstanceMemoryMB"]
        instance = Cluster(config, instance_data, http_client)
        # # 查看缓存云实例详情，获取拓扑结构
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        # 获取CFS的拓扑结构
        cfs_host = get_master_server_step(instance, "cfs")
        cfs_client = CFS(cfs_host, config)
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        # 验证数据库与CFS中的拓扑结构相同
        assert masterIp == masterIp_cfs, info_logger.error("Ip of master container is inconsistent")
        assert masterDocker == masterDocker_cfs, info_logger.error("Docker_id of master container is inconsistent")
        assert slaveIp == slaveIp_cfs, info_logger.error("Ip of slave container is inconsistent")
        assert slaveDocker == slaveDocker_cfs, info_logger.error("Docker_id of slave container is inconsistent")
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
    def test_create_ms_without_password(self, config, instance_data):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params(instance_data)
        create_params["password"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["auth"] is False
        assert cluster_detail["cacheInstanceType"] == 'master-slave'
        # domain = cluster_detail["connectionDomain"]

        # # 验证通过nlb访问实例
        # accesser = Accesser(config)
        # ping_domain_step(accesser, space_id)
        # check_access_domain_step(accesser, space_id, password)

        # 删除实例
        delete_step(redis_cap, space_id)
        time.sleep(5)

    @pytest.mark.regression
    def test_create_ms_postpaid(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        # assert cluster_detail["auth"] is True
        # assert cluster_detail["cacheInstanceType"] == 'master-slave'
        charge = cluster_detail["charge"]
        assert charge["chargeMode"] == "postpaid_by_duration"
        assert charge["chargeStatus"] == "normal"

    @pytest.mark.regression
    def test_create_ms_prepaid(self, config, instance_data):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params(instance_data)
        space_id, error = create_step(redis_cap, create_params, charge_params)
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        # 重试三次，因为可能会查不到计费信息
        for i in range(3):
            cluster_detail, error = query_detail_step(redis_cap, space_id)
            assert cluster_detail["cacheInstanceStatus"] == "running"
            # assert cluster_detail["auth"] is True
            # assert cluster_detail["cacheInstanceType"] == 'master-slave'
            if "charge" in cluster_detail:
                charge = cluster_detail["charge"]
                assert charge["chargeMode"] == "prepaid_by_duration"
                assert charge["chargeStatus"] == "normal"
                break
            time.sleep(config["wait_time"])

        # 删除实例
        delete_step(redis_cap, space_id, 1)
        time.sleep(5)

    @pytest.mark.regression
    def test_create_cluster_without_password(self, config, instance_data):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params(instance_data)
        create_params["password"] = ""
        create_params["cacheInstanceClass"] = instance_data["cache_cluster_class"]
        space_id, error = create_step(redis_cap, create_params, None)
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["auth"] is False
        assert cluster_detail["cacheInstanceType"] == 'cluster'
        # domain = cluster_detail["connectionDomain"]

        # # 验证通过nlb访问实例
        # accesser = Accesser(config)
        # ping_domain_step(accesser, space_id)
        # check_access_domain_step(accesser, space_id, password)

        # 删除实例
        delete_step(redis_cap, space_id)
        time.sleep(5)

    @pytest.mark.regression
    def test_create_cluster_with_password(self, config, instance_data, http_client, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["auth"] is True
        assert cluster_detail["cacheInstanceType"] == 'cluster'
        # domain = cluster_detail["connectionDomain"]
        capacity = cluster_detail["cacheInstanceMemoryMB"]
        cluster = Cluster(config, instance_data, http_client)
        # # 查看缓存云实例详情，获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 获取CFS的拓扑结构
        cfs_host = get_master_server_step(cluster, "cfs")
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
