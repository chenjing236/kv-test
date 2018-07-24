# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResetPassword:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_reset_password(self, created_instance, config):
        # 创建缓存云实例，创建成功
        space_id, cluster, password_default = created_instance
        # 通过NLB访问缓存云实例，输入auth默认token,可以正常访问
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password_default)

        # run reset password
        password_new = "1qaz2WSX"
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new)
        # 使用长度为8的新密码，通过NLB访问缓存云实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password_new)

        # run reset password
        time.sleep(3)
        reset_password_step(cluster, space_id, password_new + password_new)
        # 使用长度为16的新密码，通过NLB访问缓存云实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password_new + password_new)

        # run reset password
        time.sleep(3)
        reset_password_step(cluster, space_id, "")
        # 设置redis免密，通过NLB访问缓存云实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id)
