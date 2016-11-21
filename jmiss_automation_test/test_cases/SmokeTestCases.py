# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCases:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, instance_data, http_client):
        print "\n[SCENARIO] Create an instance including a master container and a slave container"
        info_logger.info("[SCENARIO] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        #创建缓存云实例
        print "[STEP1] Create an instance including a master container and a slave container"
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        space_id = create_instance_step(instance)
        print "[INFO] The instance {0} is created".format(space_id)
        info_logger.info("[INFO] The instance %s is created", space_id)
        #查看缓存云实例详细信息
        print "[STEP2] Get detailed information of the instance {0}".format(space_id)
        info_logger.info("[STEP2] Get detailed information of the instance %s", space_id)
        status, capacity = get_status_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        print "[INFO] Status of the instance {0} is {1}".format(space_id, status)
        info_logger.info("[INFO] Status of the instance %s is %s", space_id, status)
        #验证缓存云实例状态，status=100创建成功
        assert status == 100
        #查看缓存云实例详情，获取拓扑结构
        print "[STEP3] Get topology information of instance"
        info_logger.info("[STEP3] Get topology information of instance")
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp, masterPort)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp, slavePort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        #获取CFS的拓扑结构
        print "[STEP4] Get topology information of instance from CFS"
        info_logger.info("[STEP4] Get topology information of instance from CFS")
        cfs_client = CFS(config)
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp_cfs, masterPort_cfs)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp_cfs, masterPort_cfs)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp_cfs, slavePort_cfs)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_cfs, slavePort_cfs)
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterPort == masterPort_cfs, "[ERROR] Port of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slavePort == slavePort_cfs, "[ERROR] Port of slave container is inconsistent"
        #获取container的大小，验证container的大小
        container = Container(config)
        master_memory_size, slave_memory_size = get_container_memory_size(container, masterIp, masterPort, slaveIp, slavePort)
        print "[INFO] Memory size of master container is {0}".format(master_memory_size)
        info_logger.info("[INFO] Memory size of master container is %s", master_memory_size)
        print "[INFO] Memory size of slave container is {0}".format(slave_memory_size)
        assert master_memory_size == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert slave_memory_size == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        #删除缓存云实例
        print "[STEP5] Delete the instance {0}".format(space_id)
        info_logger.info("[STEP5] Delete the instance %s", space_id)
        delete_instance_step(instance, space_id)
        #assert False, "[ERROR] test error log"


    @pytest.mark.smoke
    def test_access_ap(self, config, instance_data, http_client, created_instance):
        print "\n[SCENARIO] It is successfull to access AP and to set/get key"
        info_logger.info("[SCENARIO] It is successfull to access AP and to set/get key")
        #创建缓存云实例，创建成功
        print "[STEP1] Create an instance with a master container and a slave container"
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance = created_instance
        print "[INFO] The instance {0} is created".format(space_id)
        info_logger.info("[INFO] The instance %s is created", space_id)
        #获取AP的token
        print "[STEP2] Get token for the instance {0}".format(space_id)
        info_logger.info("[STEP2] Get token for the instance %s", space_id)
        instance_info = get_detail_info_of_instance_step(instance, space_id)
        password = instance_info["password"]
        domain = instance_info["domain"]
        print "[INFO] Token is {0} for the instance {1}".format(password, space_id)
        info_logger.info("[INFO] Token is %s for the instance %s", password, space_id)
        #获取拓扑结构
        print "[STEP3] Get topology information of the instance {0}".format(space_id)
        info_logger.info("[STEP3] Get topology information of the instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp, masterPort)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp, slavePort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        #设置ACL访问规则
        print "[STEP4] Set ACL for the instance {0}".format(space_id)
        info_logger.info("[STEP4] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        #通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        print "[INFO] The list of ip of acl is {0} for the instance {1}".format(acl_ips, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        print "[STEP5] Access AP"
        info_logger.info("[STEP5] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], password)
        assert is_access_ap == True, "[ERROR] Cannot access to the ap of the instanche {0}".format(space_id)
        print "[INFO] It is succesfull to get the value by key from the instance {0}".format(space_id)
        info_logger.info("[INFO] It is succesfull to get the value by key from the instance %s", space_id)

    @pytest.mark.smoke
    def test_resize_instance(self, config, instance_data, http_client, created_instance):
        print "\n[SCENARIO] It is successfull to resize intance"
        info_logger.info("[SCENARIO] It is successfull to resize intance")
        #创建缓存云实例，创建成功
        print "[STEP1] Create an instance with a master container and a slave container"
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance = created_instance
        print "[INFO] The instance {0} is created".format(space_id)
        info_logger.info("[INFO] The instance %s is created", space_id)
        #获取原有缓存云实例的capacity
        print "[STEP2] Get the memory size of the origin instance {0}".format(space_id)
        info_logger.info("[STEP2] Get the memory size of the origin instance %s", space_id)
        instance_info = get_detail_info_of_instance_step(instance, space_id)
        capacity_origin = int(instance_info["capacity"])
        password = instance_info["password"]
        #获取拓扑结构
        print "[STEP3] Get topology information of instance {0}".format(space_id)
        info_logger.info("[STEP3] Get topology information of instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp, masterPort)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp, slavePort)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp, slavePort)
        #通过master，执行set/get key
        print "[STEP4] Set key to the master container of the instance {0}".format(space_id)
        info_logger.info("[STEP4] Set key to the master container of the instance %s", space_id)
        is_successfull, key, value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
        assert is_successfull == True
        print "[INFO] It is successful to set key to the master of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
        #执行扩容操作
        print "[STEP5] Resize the instance {0}".format(space_id)
        info_logger.info("[STEP5] Resize the instance %s", space_id)
        cfs_client = CFS(config)
        zoneId = int(instance_data["zoneId"])
        capacity = int(instance_data["capacity_resize"])
        status, capacity_new = resize_instance_step(instance, cfs_client , space_id, zoneId, capacity, config["retry_times"], int(config["wait_time"]))
        #验证扩容操作后的大小
        assert capacity_new != capacity_origin, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(space_id)
        assert capacity_new == capacity, "[ERROR] The capacity is incorrect after resizing the instance {0}".format(space_id)
        print "[INFO] It is successful to resize the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to resize the instance %s", space_id)
        #设置ACL访问规则
        print "[STEP4] Set ACL for the instance {0}".format(space_id)
        info_logger.info("[STEP4] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        #通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        print "[INFO] The list of ip of acl is {0} for the instance {1}".format(acl_ips, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        #通过AP访问获取key
        print "[STEP6] Get key from the instance reiszed {0}".format(space_id)
        info_logger.info("[STEP6] Get key from the instance reiszed %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instanche {0}".format(space_id)
        print "[INFO] It is successful to get value from the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to get value from the instance %s", space_id)

    @pytest.mark.smoke
    def test_failover(self, config, instance_data, http_client, created_instance):
        print "\n[SCENARIO] It is successfull to run failover master"
        info_logger.info("[SCENARIO] It is successfull to run failover master")
        #创建缓存云实例，创建成功
        print "[STEP1] Create an instance with a master container and a slave container"
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance = created_instance
        print "[INFO] The instance {0} is created".format(space_id)
        info_logger.info("[INFO] The instance %s is created", space_id)
        #获取原有缓存云实例的capacity
        print "[STEP2] Get the token of the origin instance {0}".format(space_id)
        info_logger.info("[STEP2] Get the token of the origin instance %s", space_id)
        instance_info = get_detail_info_of_instance_step(instance, space_id)
        password = instance_info["password"]
        print "[INFO] The token of the instance {0} is {1}".format(space_id, password)
        info_logger.info("[INFO] The token of the instance %s is %s", space_id, password)
        #获取拓扑结构
        print "[STEP3] Get topology information of the instance {0}".format(space_id)
        info_logger.info("[STEP3] Get topology information of the instance %s", space_id)
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp, masterPort)
        info_logger.info("[INFO] Information of master container is %s:%s", masterIp, masterPort)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp, slavePort)
        info_logger.info("[INFO] Information of slave container is %s:%s", masterIp, masterPort)
        #通过AP访问缓存云实例，执行set/get key
        print "[STEP4] Set key to the master container of the instance {0}".format(space_id)
        info_logger.info("[STEP4] Set key to the master container of the instance %s", space_id)
        is_successfull, key,value = access_container_step(masterIp, masterPort, slaveIp, slavePort)
        assert is_successfull == True
        print "[INFO] It is successful to set key to the master of the instance {0}".format(space_id)
        info_logger.info("[INFO] It is successful to set key to the master of the instance %s", space_id)
        #run master failover
        print "[STEP5] Run failover for master container"
        info_logger.info("[STEP5] Run failover for master container")
        cfs_client = CFS(config)
        container = Container(config)
        retry_times = int(config["retry_getting_topology_from_cfs"])
        wait_time = int(config["wait_time"])
        is_failover, master_ip_new, master_port_new, slaveIp_new, slavePort_new = run_failover_container_step(instance, cfs_client, container, space_id, masterIp, masterPort, retry_times, wait_time)
        assert is_failover == True, "[ERROR] Run master failover is failed"
        print "[INFO] Information of master container is {0}:{1}".format(master_ip_new, master_port_new)
        info_logger.info("[INFO] Information of master container is %s:%s", master_ip_new, master_port_new)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp_new, slavePort_new)
        info_logger.info("[INFO] Information of slave container is %s:%s", slaveIp_new, slavePort_new)
        #设置ACL访问规则
        print "[STEP6] Set ACL for the instance {0}".format(space_id)
        info_logger.info("[STEP6] Set ACL for the instance %s", space_id)
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(instance, space_id, ips)
        #通过AP访问缓存云实例，输入auth,可以正常访问
        acl_ips = get_acl_step(instance, space_id)
        print "[INFO] The list of ip of acl is {0} for the instance {1}".format(acl_ips, space_id)
        info_logger.info("[INFO] The list of ip of acl is %s for the instance %s", acl_ips, space_id)
        #通过AP访问获取key
        print "[STEP7] Get key from the instance reiszed {0}".format(space_id)
        info_logger.info("[STEP7] Get key from the instance reiszed %s", space_id)
        value_from_ap = get_key_from_ap_step(config["ap_host"], config["ap_port"], password, key)
        assert value_from_ap == value, "[ERROR] Cannot get the value from the ap of the instanche {0}".format(space_id)
        #通过AP访问缓存云实例，执行set/get key
        print "[STEP7] Access AP"
        info_logger.info("[STEP7] Access AP")
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], password)
        assert is_access_ap == True, "[ERROR] Cannot access to the ap of the instanche {0}".format(space_id)
        print "[INFO] It is succesfull to get the value by key {0} from the instance {1}".format(key,space_id)
        info_logger.info("[INFO] It is succesfull to get the value by key %s from the instance %s", key,space_id)