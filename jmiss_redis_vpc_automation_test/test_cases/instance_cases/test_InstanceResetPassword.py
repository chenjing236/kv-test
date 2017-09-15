# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResetPassword:
    @pytest.mark.resetpassword
    def test_reset_password(self, created_instance):
        info_logger.info("[SCENARIO] Start to test reset password")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create a cluster with a set of master and slave containers")
        space_id, instance, password_default = created_instance
        info_logger.info("[INFO] The cluster %s is created, the password is %s", space_id, password_default)
        # 通过AP访问缓存云实例，输入auth默认token,可以正常访问

        # run reset password
        info_logger.info("[STEP2] Start to reset password of the cluster to 8 characters long")
        password_new = "1qaz2WSX"
        time.sleep(3)
        reset_password_step(instance, space_id, password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new))
        # 使用新密码，通过AP访问缓存云实例

        # run reset password
        info_logger.info("[STEP3] Start to reset password of the cluster to 16 characters long")
        time.sleep(3)
        reset_password_step(instance, space_id, password_new + password_new)
        info_logger.info("[INFO] Reset password successfully! The password is {0}".format(password_new + password_new))
        # 使用新密码，通过AP访问缓存云实例
