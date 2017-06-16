# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestFailoverCluster:
    # @pytest.mark.smoke
    # def test_failover_master(self, config, created_instance):
    #     info_logger.info("[SCENARIO] Start to run failover master")
    #     # 创建缓存云实例，创建成功
    #     info_logger.info("[STEP1] Create an instance with a master container and a slave container")
    #     space_id, instance, password = created_instance
    #     info_logger.info("[INFO] The instance %s is created", space_id)
    #     info_logger.info("[INFO] The password of the instance %s is %s", space_id, password)
    #     # 获取拓扑结构
    #     info_logger.info("[STEP2] Get topology information of the instance %s", space_id)
    #     masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
    #     info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
    #     info_logger.info("[INFO] Information of slave container is %s:%s", masterIp, masterPort)
    #     # 通过AP访问缓存云实例，执行set/get key
    #     info_logger.info("[STEP3] Set key to the master container of the instance %s", space_id)
    #     is_successful, key, value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
    #     assert is_successful is True
    #     info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
    #     # run master failover
    #     info_logger.info("[STEP4] Run failover for master container")
    #     cfs_client = CFS(config)
    #     container = Container(config)
    #     retry_times = int(config["retry_getting_topology_from_cfs"])
    #     wait_time = int(config["wait_time"])
    #     is_failover, master_ip_new, master_port_new, slaveIp_new, slavePort_new = run_failover_container_step(
    #         instance, cfs_client, container, space_id, 2, masterIp, masterPort, retry_times, wait_time)
    #     assert is_failover is True, "[ERROR] Run master failover is failed"
    #     info_logger.info("[INFO] Information of master container is %s:%s", master_ip_new, master_port_new)
    #     info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_new, slavePort_new)
    #     # 设置ACL访问规则
    #     info_logger.info("[STEP5] Set ACL for the instance %s", space_id)
    #     ip = get_local_ip()
    #     ips = [ip]
    #     set_acl_step(instance, space_id, ips)
    #     # 通过AP访问缓存云实例，输入auth,可以正常访问
    #     acl_ips = get_acl_step(instance, space_id)
    #     info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
    #     # 通过AP访问获取key
    #     info_logger.info("[STEP6] Get key from the failover instance %s", space_id)
    #     value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
    #     assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
    #     # 通过AP访问缓存云实例，执行set/get key
    #     info_logger.info("[STEP7] Access AP")
    #     is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
    #     assert is_access_ap is True, "[ERROR] Cannot access to the ap of the instance {0}".format(space_id)
    #     info_logger.info("[INFO] It is successful to get the value by key %s from the instance %s", key, space_id)

    @pytest.mark.smoke
    def test_failover_slave(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to run failover slave")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of the instance %s is %s", space_id, password)
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        info_logger.info("[INFO] Information of slave container is %s:%s", masterIp, masterPort)
        # 通过AP访问缓存云实例，执行set/get key
        info_logger.info("[STEP3] Set key to the master container of the instance %s", space_id)
        is_successful, key, value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
        assert is_successful is True
        info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
        # run slave failover
        info_logger.info("[STEP4] Run failover for slave container")
        cfs_client = CFS(config)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        is_failover, master_ip_new, master_port_new, slaveIp_new, slavePort_new = run_failover_container_step(
            instance, cfs_client, container, space_id, 1, slaveIp, slavePort, retry_times, wait_time)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        info_logger.info("[INFO] Information of master container is %s:%s", master_ip_new, master_port_new)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_new, slavePort_new)
        # 设置ACL访问规则
        info_logger.info("[STEP5] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        # 通过AP访问获取key
        info_logger.info("[STEP6] Get key from the failover instance %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
        # 通过AP访问缓存云实例，执行set/get key
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key %s from the instance %s", key, space_id)

