# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestSmokeCases:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        space_id, password = create_instance_with_password_step(instance, instance_data["password"])
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the instance %s", space_id)
        status, capacity = get_status_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        info_logger.info("[INFO] Status of the instance %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP3] Get topology information of instance")
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        # 获取CFS的拓扑结构
        info_logger.info("[STEP4] Get topology information of instance from CFS")
        cfs_client = CFS(config)
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp_cfs, masterPort_cfs)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_cfs, slavePort_cfs)
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterPort == masterPort_cfs, "[ERROR] Port of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slavePort == slavePort_cfs, "[ERROR] Port of slave container is inconsistent"
        # 获取container的大小，验证container的大小
        container = Container(config)
        master_memory_size, slave_memory_size = get_container_memory_size_step(container, masterIp, masterPort, slaveIp, slavePort)
        info_logger.info("[INFO] Memory size of master container is %s", master_memory_size)
        assert master_memory_size == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert slave_memory_size == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        # 删除缓存云实例
        info_logger.info("[STEP5] Delete the instance %s", space_id)
        delete_instance_step(instance, space_id)
        # assert False, "[ERROR] test error log"

    @pytest.mark.smoke
    def test_access_ap(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to access AP and to set/get key")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        # 获取AP的token
        # info_logger.info("[STEP2] Get token for the instance %s", space_id)
        # instance_info = get_detail_info_of_instance_step(instance, space_id)
        # password = instance_info["password"]
        # domain = instance_info["domain"]
        info_logger.info("[INFO] The password is %s for the instance %s", password, space_id)
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        # 设置ACL访问规则
        info_logger.info("[STEP3] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        info_logger.info("[STEP4] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key from the instance %s", space_id)

    @pytest.mark.smoke
    def test_resize_instance(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] Start to resize instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        # 获取原有缓存云实例的capacity
        info_logger.info("[STEP2] Get the memory size of the origin instance %s", space_id)
        instance_info = get_detail_info_of_instance_step(instance, space_id)
        capacity_origin = int(instance_info["capacity"])
        # password = instance_info["password"]
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
        # 执行扩容操作
        info_logger.info("[STEP5] Resize the instance %s", space_id)
        cfs_client = CFS(config)
        zoneId = int(instance_data["zoneId"])
        capacity = int(instance_data["capacity_resize"])
        status, capacity_new = resize_instance_step(instance, cfs_client, space_id, zoneId, capacity, config["retry_times"], int(config["wait_time"]))
        # 验证扩容操作后的大小
        assert capacity_new != capacity_origin, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(space_id)
        assert capacity_new == capacity, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to resize the instance %s", space_id)
        # 设置ACL访问规则
        info_logger.info("[STEP4] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        # 通过AP访问获取key
        info_logger.info("[STEP6] Get key from the instance resized %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get value from the instance %s", space_id)

    @pytest.mark.smoke
    def test_failover(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to run failover master")
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
        # run master failover
        info_logger.info("[STEP4] Run failover for master container")
        cfs_client = CFS(config)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        is_failover, master_ip_new, master_port_new, slaveIp_new, slavePort_new = run_failover_container_step(instance, cfs_client, container, space_id, masterIp, masterPort, retry_times, wait_time)
        assert is_failover is True, "[ERROR] Run master failover is failed"
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
        info_logger.info("[STEP6] Get key from the instance resized %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
        # 通过AP访问缓存云实例，执行set/get key
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get the value by key %s from the instance %s", key, space_id)

    @pytest.mark.smoke
    def test_reset_password(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to test reset password")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster, password_default = created_instance
        info_logger.info("The cluster %s is created, the password is %s", space_id, password_default)
        # 设置ACL访问规则
        info_logger.info("[STEP2] Set ACL for the cluster {0}".format(space_id))
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth默认token,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP3] Access AP with default token")
        wait_time = int(config["wait_time"])
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password_default)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
        # run reset password
        info_logger.info("[STEP4] Start to reset password of the cluster to 8 characters long")
        password_new = "1qaz2WSX"
        reset_password_step(cluster, space_id, password_new)
        info_logger.info("Reset password successfully!")
        # 使用新密码，通过AP访问缓存云实例
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP5] Access AP with new password")
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password_new)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap with new password of the cluster {0}".format(
            space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
        # run reset password
        info_logger.info("[STEP6] Start to reset password of the cluster to 16 characters long")
        reset_password_step(cluster, space_id, password_new + password_new)
        info_logger.info("Reset password successfully!")
        # 使用新密码，通过AP访问缓存云实例
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP7] Access AP with new password")
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"],
                                      space_id + ":" + password_new + password_new)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap with new password of the cluster {0}".format(
            space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
