# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestAccessAP:
    @pytest.mark.accessap
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
        # 设置system acl的enable为false，不能进行访问
        info_logger.info("[STEP5] Set system acl enable false")
        set_system_acl_step(instance, space_id, False)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is False, "[ERROR] Enable=false, but still accessible"
        info_logger.info("[INFO] Access ap failure when enable is false")
        # 设置system acl的enable为true，可以正常访问
        info_logger.info("[STEP6] Set system acl enable true")
        set_system_acl_step(instance, space_id, True)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the instance {0}".format(space_id)
        info_logger.info("[INFO] Access ap successfully when enable is true")
