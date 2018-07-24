# coding:utf-8
from conftest import *


class TestSmokeCases:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, instance_data, http_client):
        print "\n"
        info_logger.info("[SCENARIO] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        space_id, operation_id, password = create_instance_step(instance)
        info_logger.info("[INFO] The instance {0} is created, its password is {1}".format(space_id, password))
        # 查看创建操作结果，验证创建成功
        info_logger.info("[STEP2] Get creation result of the instance {0}".format(space_id))
        is_success = get_operation_result_step(instance, space_id, operation_id)
        assert is_success is True, "[INFO] Get the right operation result, create instance successfully"
        # 设置资源acl
        info_logger.info("[STEP3] Set enable acl for the instance {0}".format(space_id))
        set_acl_step(instance, space_id)
        info_logger.info("[INFO] Set acl successfully!")
        # 查看redis详情，验证缓存云实例状态，status=100创建成功
        info_logger.info("[STEP4] Get detail info of the instance {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        assert detail_info["status"] == 100, "[ERROR] The cluster status is not 100!"
        assert detail_info["zone"] != 'clsdocker', "[ERROR] The cluster zone is clsdocker!"
        info_logger.info("[INFO] Get the right detail info, the status of cluster {0} is 100".format(space_id))
        capacity = detail_info["capacity"]
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP5] Get topology information of instance")
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 获取CFS的拓扑结构
        info_logger.info("[STEP6] Get topology information of instance from CFS")
        cfs_host = get_master_cfs_step(instance)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(
            cfs_client, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp_cfs, masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp_cfs, slaveDocker_cfs))
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterDocker == masterDocker_cfs, "[ERROR] Docker_id of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slaveDocker == slaveDocker_cfs, "[ERROR] Docker_id of slave container is inconsistent"
        # 获取container的大小，验证container的大小
        info_logger.info("[STEP7] Get container info from nova agent")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master[
                   "total"] == capacity * 1024, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave[
                   "total"] == capacity * 1024, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] Memory size of master and slave container is {0}".format(capacity))
        # 删除缓存云实例
        info_logger.info("[STEP8] Delete the instance {0}".format(space_id))
        delete_instance_step(instance, space_id)

    # test_access_ap

    @pytest.mark.smoke
    def test_resize_instance(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to resize instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的flavor
        info_logger.info("[STEP2] Get the flavor of the origin instance {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin instance is [{}]".format(flavor_id))
        # 执行扩容操作
        info_logger.info("[STEP3] Resize the instance {0}".format(space_id))
        flavor_id_resize = instance_data["flavorIdResize"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after resizing the instance {0}" \
            .format(space_id)
        assert flavor_id_new == flavor_id_resize, "[ERROR] The flavor is incorrect after resizing the instance {0}" \
            .format(space_id)
        assert status == 100, "[ERROR] The status of instance [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of instance {0} after resize".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp, slaveDocker))
        info_logger.info("[STEP5] Check the capacity of instance after resize")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master[
                   "total"] == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave[
                   "total"] == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to resize the instance [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))

    @pytest.mark.smoke
    def test_reduce_instance(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to reduce instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的flavor
        info_logger.info("[STEP2] Get the memory size of the origin instance {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin instance is [{}]".format(flavor_id))
        # 执行缩容操作
        info_logger.info("[STEP3] Reduce the instance {0}".format(space_id))
        flavor_id_reduce = instance_data["flavorIdReduce"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_reduce)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after reducing the instance {0}" \
            .format(space_id)
        assert flavor_id_new == flavor_id_reduce, "[ERROR] The flavor is incorrect after reducing the instance {0}" \
            .format(space_id)
        assert status == 100, "[ERROR] The status of instance [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of instance [{0}] after reduce".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp, slaveDocker))
        info_logger.info("[STEP5] Check the capacity of instance after reduce")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master[
                   "total"] == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave[
                   "total"] == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to reduce the instance [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))

    @pytest.mark.smoke
    def test_failover_master(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to run failover master")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the instance {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，执行set/get key
        # run master failover
        info_logger.info("[STEP3] Run failover for master container")
        cfs_host = get_master_cfs_step(instance)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, masterDocker, container, cfs_client, 2)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        logger_info.info("[INFO] It is successful to run master failover")
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(
            cfs_client, space_id)
        info_logger.info(
            "[INFO] Information of master container after master failover is {0}: [{1}]".format(masterIp_cfs,
                                                                                                masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container after master failover is {0}: [{1}]".format(slaveIp_cfs,
                                                                                                            slaveDocker_cfs))
        assert masterDocker != masterDocker_cfs
        assert slaveDocker == slaveDocker_cfs
        info_logger.info("[INFO] Test master failover successfully!")

    @pytest.mark.smoke
    def test_failover_slave(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to run failover slave")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the instance {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，执行set/get key
        # run master failover
        info_logger.info("[STEP3] Run failover for slave container")
        cfs_host = get_master_cfs_step(instance)
        info_logger.info("[INFO] The master cfs is {0}".format(cfs_host))
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, slaveDocker, container, cfs_client, 1)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        logger_info.info("[INFO] It is successful to run slave failover")
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(
            cfs_client, space_id)
        info_logger.info(
            "[INFO] Information of master container after slave failover is {0}: [{1}]".format(masterIp_cfs,
                                                                                               masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container after slave failover is {0}: [{1}]".format(slaveIp_cfs,
                                                                                                           slaveDocker_cfs))
        assert masterDocker == masterDocker_cfs
        assert slaveDocker != slaveDocker_cfs
        info_logger.info("[INFO] Test slave failover successfully!")

    @pytest.mark.smoke
    def test_reset_password(self, created_instance):
        info_logger.info("[SCENARIO] Start to test reset password")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster, password_default = created_instance
        info_logger.info("[INFO] The cluster {0} is created, the password is {1}".format(space_id, password_default))
        # 通过AP访问缓存云实例，输入auth默认token,可以正常访问

        # run reset password
        info_logger.info("[STEP2] Start to reset password of the cluster to 8 characters long")
        password_new = "1qaz2WSX"
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new))
        # 使用新密码，通过AP访问缓存云实例

        # run reset password
        info_logger.info("[STEP3] Start to reset password of the cluster to 16 characters long")
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new + password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new + password_new))
        # 使用新密码，通过AP访问缓存云实例
