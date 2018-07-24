# coding:utf-8
from conftest import *


class TestSmokeCasesOfCluster:

    @pytest.mark.smoke
    def test_create_cluster(self, config, instance_data, http_client):
        print "\n"
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

    @pytest.mark.smoke
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
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after resizing the cluster {0}" \
            .format(space_id)
        assert flavor_id_new == flavor_id_resize, "[ERROR] The flavor is incorrect after resizing the cluster {0}" \
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

    @pytest.mark.smoke
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

    @pytest.mark.smoke
    def test_failover_master(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] It is successful to run failover master of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # run master failover
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["masterDocker"], container, cfs_client,
                                                  2)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        logger_info.info("[INFO] It is successful to run master failover")
        info_logger.info("[STEP4] Get topology information from CFS {0}".format(space_id))
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Master container of shard_{0} after master failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["masterIp"],
                                 shards_cfs[failover_num]["masterDocker"]))
        info_logger.info("[INFO] Slave container of shard_{0} after master failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["slaveIp"],
                                 shards_cfs[failover_num]["slaveDocker"]))
        assert shards[failover_num]["masterDocker"] != shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] == shards_cfs[failover_num]["slaveDocker"]
        info_logger.info("[INFO] Test master failover successfully!")

    @pytest.mark.smoke
    def test_failover_slave(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] It is successful to run failover slave of a shard")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of slave container and a slave container")
        space_id, cluster, password = created_instance
        info_logger.info("[INFO] The cluster {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the cluster {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of cluster {0}".format(space_id))
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shard_count))
        for i in range(0, shard_count):
            info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # run master failover
        cfs_host = get_master_cfs_step(cluster)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("[INFO] To stop the slave container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["slaveDocker"], container, cfs_client,
                                                  1)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        logger_info.info("[INFO] It is successful to run slave failover")
        info_logger.info("[STEP4] Get topology information from CFS {0}".format(space_id))
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Master container of shard_{0} after slave failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["masterIp"],
                                 shards_cfs[failover_num]["masterDocker"]))
        info_logger.info("[INFO] Slave container of shard_{0} after slave failover is {1}: [{2}]"
                         .format(failover_num + 1, shards_cfs[failover_num]["slaveIp"],
                                 shards_cfs[failover_num]["slaveDocker"]))
        assert shards[failover_num]["masterDocker"] == shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] != shards_cfs[failover_num]["slaveDocker"]
        info_logger.info("[INFO] Test slave failover successfully!")

    @pytest.mark.smoke
    def test_reset_password(self, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to run reset password")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster, password_default = created_instance
        info_logger.info("[INFO] The cluster {0} is created, the password is {1}".format(space_id, password_default))
        # 通过AP访问缓存云实例，输入auth默认token,可以正常访问

        # run reset password
        info_logger.info("[STEP4] Start to reset password of the cluster to 8 characters long")
        password_new = "1qaz2WSX"
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new))
        # 使用新密码，通过AP访问缓存云实例

        # run reset password
        info_logger.info("[STEP6] Start to reset password of the cluster to 16 characters long")
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new + password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new))
        # 使用新密码，通过AP访问缓存云实例
