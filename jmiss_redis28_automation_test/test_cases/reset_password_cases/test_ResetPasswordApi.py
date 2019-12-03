# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestResetPasswordApi:
    @pytest.mark.regression
    def test_reset_password_null(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码为空
        password_new = None
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
        info_logger.info("Test reset password to null successfully!")

    @pytest.mark.regression
    def test_reset_password_shorter_than_8(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码失败
        password_new = "1qaz3ED"
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用原来的密码访问资源
        info_logger.info("Test reset password shorter than 8 successfully!")

    @pytest.mark.regression
    def test_reset_password_longer_than_16(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码失败
        password_new = "1qaz3EDC1qaz3EDC1"
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用原来的密码访问资源
        info_logger.info("Test reset password longer than 16 successfully!")

    @pytest.mark.regression
    def test_reset_password_not_contain_capital_letters(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码失败
        password_new = "1qaz3edc"
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用原来的密码访问资源
        info_logger.info("Test reset password not contain capital letters successfully!")

    @pytest.mark.regression
    def test_reset_password_not_contain_lowercase_letters(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码失败
        password_new = "1QAZ3EDC"
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用原来的密码访问资源
        info_logger.info("Test reset password not contain lowercase letters successfully!")

    @pytest.mark.regression
    def test_reset_password_not_contain_numbers(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码失败
        password_new = "qazWSXedc"
        error = reset_password_step(redis_cap, space_id, password_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用原来的密码访问资源
        info_logger.info("Test reset password not contain numbers successfully!")

    @pytest.mark.regression
    def test_reset_password_length_equal_8(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = "1qaz3EDC"
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
        info_logger.info("Test reset password length equal 8 successfully!")

    @pytest.mark.regression
    def test_reset_password_length_equal_16(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，auth=True
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["auth"] is True
        # todo: 验证使用密码访问资源
        # 修改资源密码
        password_new = "1qaz3EDC1qaz3EDC"
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
        info_logger.info("Test reset password length equal 16 successfully!")
