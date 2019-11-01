# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestResetPassword:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_reset_password_ms_not_null(self, instance_data, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = set_password(instance_data["password"])
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
