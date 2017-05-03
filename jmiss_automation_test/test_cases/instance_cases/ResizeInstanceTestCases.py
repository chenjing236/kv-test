# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResizeInstance:

    @pytest.mark.resizeinstance
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
        status, capacity_new = resize_instance_step(instance, cfs_client, space_id, zoneId, capacity,
                                                    config["retry_times"], int(config["wait_time"]))
        # 验证扩容操作后的大小
        assert capacity_new != capacity_origin, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(
            space_id)
        assert capacity_new == capacity, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(
            space_id)
        info_logger.info("[INFO] It is successful to resize the instance %s, the capacity is correct", space_id)
        # 设置ACL访问规则
        info_logger.info("[STEP6] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        # 通过AP访问获取key
        info_logger.info("[STEP7] Get key from the instance resized %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get value from the instance %s", space_id)

    @pytest.mark.resizeinstance
    def test_reduce_instance(self, config, instance_data, created_instance):
        info_logger.info("[SCENARIO] Start to reduce instance")
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
        # 执行缩容操作
        info_logger.info("[STEP5] Reduce the instance %s", space_id)
        cfs_client = CFS(config)
        zoneId = int(instance_data["zoneId"])
        capacity = int(instance_data["capacity_reduce"])
        status, capacity_new = resize_instance_step(instance, cfs_client, space_id, zoneId, capacity,
                                                    config["retry_times"], int(config["wait_time"]))
        # 验证缩容操作后的大小
        assert capacity_new != capacity_origin, "[ERROR] The capacity is incorrect after reducing the instance {0}".format(
            space_id)
        assert capacity_new == capacity, "[ERROR] The capacity is incorrect after reducing the instance {0}".format(
            space_id)
        info_logger.info("[INFO] It is successful to reduce the instance %s, the capacity is correct", space_id)
        # 设置ACL访问规则
        info_logger.info("[STEP6] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        # 通过AP访问获取key
        info_logger.info("[STEP7] Get key from the instance reduced %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get value from the instance %s", space_id)
