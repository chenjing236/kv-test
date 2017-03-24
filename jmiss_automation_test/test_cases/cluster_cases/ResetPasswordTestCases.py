# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResetPassword:
    @pytest.mark.smoke
    def test_reset_password(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to run reset password")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, cluster, password_default = created_instance
        info_logger.info("The cluster %s is created, the password is %s", space_id, password_default)
        # 获取缓存云实例的默认密码/token
        # info_logger.info("[STEP2] Get the default token of the origin cluster %s", space_id)
        # instance_info = get_detail_info_of_instance_step(cluster, space_id)
        # password_default = instance_info["password"]
        info_logger.info("The default token of the cluster %s is %s", space_id, password_default)
        # 设置ACL访问规则
        info_logger.info("[STEP3] Set ACL for the cluster {0}".format(space_id))
        ip = get_local_ip()
        ips = [ip]
        set_acl_step(cluster, space_id, ips)
        # 通过AP访问缓存云实例，输入auth默认token,可以正常访问
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP4] Access AP with default token")
        wait_time = int(config["wait_time"])
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password_default)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
        # run reset password
        info_logger.info("[STEP5] Start to reset password of the cluster to 8 characters long")
        password_new = "1qaz2WSX"
        reset_password_step(cluster, space_id, password_new)
        info_logger.info("Reset password successfully!")
        # 使用新密码，通过AP访问缓存云实例
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP6] Access AP with new password")
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password_new)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap with new password of the cluster {0}".format(space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
        # run reset password
        info_logger.info("[STEP7] Start to reset password of the cluster to 16 characters long")
        reset_password_step(cluster, space_id, password_new + password_new)
        info_logger.info("Reset password successfully!")
        # 使用新密码，通过AP访问缓存云实例
        acl_ips = get_acl_step(cluster, space_id)
        info_logger.info("The list of ip of acl is %s for the cluster %s", acl_ips, space_id)
        info_logger.info("[STEP8] Access AP with new password")
        time.sleep(wait_time)
        is_access_ap = access_ap_step(config["ap_host"], config["ap_port"], space_id + ":" + password_new + password_new)
        assert is_access_ap is True, "[ERROR] Cannot access to the ap with new password of the cluster {0}".format(
            space_id)
        info_logger.info("It is successful to get the value by key from the cluster %s", space_id)
