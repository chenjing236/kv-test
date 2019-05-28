# coding:utf-8
from BasicTestCase import *


class TestUnitTest:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_unit_test(self, created_instance):
        # 创建缓存云实例，创建成功
        space_id, cluster, password_default, accesser = created_instance
        # 通过domain访问缓存云实例，输入auth默认token,可以正常访问
        check_access_domain_step(accesser, space_id, password_default)

        # 设置密码为免密，用于执行redis unit test
        reset_password_step(cluster, space_id, "")
        # 执行redis unit test
        exec_unit_test_step(accesser, space_id)

        # 将密码设置回创建时的密码，不影响其他用例的执行
        reset_password_step(cluster, space_id, password_default)
        # 设置redis免密，通过domain访问缓存云实例
        check_access_domain_step(accesser, space_id)
