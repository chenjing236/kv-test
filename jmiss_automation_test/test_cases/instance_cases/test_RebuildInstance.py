# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestRebuildInstance:

    # @pytest.mark.rebuildinstance
    # def test_rebuild_repair_instance(self, config, created_instance):
    #     info_logger.info("[SCENARIO] Start to test rebuild repair instance")
    #     # 创建缓存云实例，创建成功
    #     info_logger.info("[STEP] Create an instance with a master container and a slave container")
    #     space_id, instance, password = created_instance
    #     info_logger.info("[INFO] The instance %s is created", space_id)
    #     # 获取拓扑结构
    #     info_logger.info("[STEP3] Get topology information of instance %s", space_id)
    #     masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
    #     info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
    #     info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
    #     # 通过master，执行set/get key
    #     info_logger.info("[STEP4] Set key to the master container of the instance %s", space_id)
    #     is_successful, key, value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
    #     assert is_successful is True
    #     info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
    #     # 执行rebuild流程（删除master和slave container，使资源状态变为101）
    #     cfs_client = CFS(config)
    #     docker_client = Container(config)
    #     run_rebuild_repair_step(instance, space_id, docker_client, cfs_client)
    #     # 设置ACL访问规则
    #     info_logger.info("[STEP5] Set ACL for the instance %s", space_id)
    #     ip = get_local_ip()
    #     ips = [ip]
    #     set_acl_step(instance, space_id, ips)
    #     # 通过AP访问缓存云实例，输入auth,可以正常访问
    #     acl_ips = get_acl_step(instance, space_id)
    #     info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
    #     # 通过AP访问获取key
    #     info_logger.info("[STEP6] Get key from the rebuild repair instance %s", space_id)
    #     value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
    #     assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
    #     info_logger.info("[INFO] The value from rebuild repair instance is right")
    #     info_logger.info("[INFO] Test rebuild repair instance successfully!")

    @pytest.mark.rebuildinstance
    def test_rebuild_clone_instance(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] Start to test rebuild clone instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        # 获取拓扑结构
        info_logger.info("[STEP3] Get topology information of instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        # 通过master，执行set/get key
        info_logger.info("[STEP4] Set key to the master container of the instance %s", space_id)
        is_successful, key, value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
        assert is_successful is True
        info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
        # 执行clone操作
        info_logger.info("[INFO] Start to run rebuild clone instance")
        space_id_clone = run_rebuild_clone_step(instance, space_id)
        # 设置ACL访问规则,验证clone后数据正确性
        info_logger.info("[STEP5] Set ACL for the instance %s", space_id_clone)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id_clone, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id_clone)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id_clone)
        # 通过AP访问获取key
        info_logger.info("[STEP6] Get key from the rebuild clone instance %s", space_id_clone)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id_clone + ":" + instance_data["password"], key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id_clone)
        info_logger.info("[INFO] The value from rebuild clone instance is right")
        # 删除clone的instance
        info_logger.info("[INFO] Delete the cloned instance")
        instance.delete_instance(space_id_clone)
        info_logger.info("[INFO] Test rebuild clone instance successfully!")


    #
    # @pytest.mark.rebuildinstance
    # def test_rebuild_upgrade_instance(self, config, instance_data, created_instance):
    #     info_logger.info("[SCENARIO] Start to reduce instance")
    #     # 创建缓存云实例，创建成功
    #     info_logger.info("[STEP1] Create an instance with a master container and a slave container")
    #     space_id, instance, password = created_instance
    #     info_logger.info("[INFO] The instance %s is created", space_id)
