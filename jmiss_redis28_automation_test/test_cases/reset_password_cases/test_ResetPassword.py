# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestResetPassword:
    @pytest.mark.regression
    def test_reset_password_ms_null(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=False
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        info_logger.info("Test reset password of master-slave instance to null successfully!")

    @pytest.mark.regression
    def test_reset_password_cluster_null(self, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=False
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        info_logger.info("Test reset password of cluster to null successfully!")

    @pytest.mark.newsmoke
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
        info_logger.info("Test reset password of master-slave instance not null successfully!")

    @pytest.mark.regression
    def test_reset_password_cluster_not_null(self, instance_data, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
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
        info_logger.info("Test reset password of cluster not null successfully!")

    @pytest.mark.regression
    def test_reset_password_null_to_pwd(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=False
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        info_logger.info("Test reset password from null to not null successfully!")

    @pytest.mark.regression
    def test_reset_password_pwd_to_null(self, instance_data, created_instance):
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
        # 修改资源密码为免密
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=False
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        info_logger.info("Test reset password from not null to null successfully!")

    @pytest.mark.regression
    def test_reset_password_null_to_null(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = ""
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=False
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is False
        # todo: 验证使用密码访问资源
        # 恢复资源密码
        error = reset_password_step(redis_cap, space_id, password)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        info_logger.info("Test reset password from null to null successfully!")

    @pytest.mark.regression
    def test_reset_password_pwd_to_pwd(self, instance_data, created_instance):
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
        # 修改资源密码
        password_new_2 = set_password(instance_data["password"])
        error = reset_password_step(redis_cap, space_id, password_new_2)
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
        info_logger.info("Test reset password from not null to not null successfully!")
