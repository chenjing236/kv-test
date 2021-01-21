# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryConfig:
    @pytest.mark.newsmoke
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_query_config(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取自定义参数列表
        config_list, error = query_config_step(redis_cap, space_id)
        assert error is None
        assert len(config_list) != 0

    @pytest.mark.regression
    def test_query_config_with_empty_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = None
        config_list, error = query_config_step(redis_cap, space_id)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_query_config_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = "redis-error"
        config_list, error = query_config_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_config_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = instance_data["deleted_space"]
        config_list, error = query_config_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
