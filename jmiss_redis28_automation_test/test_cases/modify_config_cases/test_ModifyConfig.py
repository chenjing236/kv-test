# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestModifyConfig:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_modify_config_with_part_of_config(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改自定义参数
        redis_config = [{"configName": "hash-max-ziplist-value", "configValue": "138"},
                        {"configName": "hash-max-ziplist-entries", "configValue": "522"},
                        {"configName": "list-max-ziplist-entries", "configValue": "510"},
                        {"configName": "list-max-ziplist-value", "configValue": "110"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error is None
        # 获取自定义参数列表，验证自定义参数修改正确
        config_list, error = query_config_step(redis_cap, space_id)
        assert error is None
        assert len(config_list) != 0
        # 校验已修改的自定义参数一致
        for config_member in redis_config:
            assert config_member in config_list
        # todo: 访问redis验证配置正确设置

    @pytest.mark.regression
    def test_modify_config_with_all_config(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改自定义参数
        redis_config = [{"configName": "maxmemory-policy", "configValue": "volatile-random"},
                        {"configName": "hash-max-ziplist-entries", "configValue": "1024"},
                        {"configName": "hash-max-ziplist-value", "configValue": "128"},
                        {"configName": "list-max-ziplist-entries", "configValue": "1024"},
                        {"configName": "list-max-ziplist-value", "configValue": "128"},
                        {"configName": "set-max-intset-entries", "configValue": "1024"},
                        {"configName": "zset-max-ziplist-entries", "configValue": "256"},
                        {"configName": "zset-max-ziplist-value", "configValue": "128"},
                        {"configName": "slowlog-log-slower-than", "configValue": "5000"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error is None
        # 获取自定义参数列表，验证自定义参数修改正确
        config_list, error = query_config_step(redis_cap, space_id)
        assert error is None
        assert len(config_list) != 0
        # 校验已修改的自定义参数一致
        for config_member in redis_config:
            assert config_member in config_list
        # todo: 访问redis验证配置正确设置

    @pytest.mark.regression
    def test_modify_config_with_empty_config(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改自定义参数
        redis_config = []
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "empty" in error.message

    @pytest.mark.regression
    def test_modify_config_with_error_config_name(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改自定义参数
        redis_config = [{"configName": "error-config-name", "configValue": "volatile-random"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message

    @pytest.mark.regression
    def test_modify_config_with_error_config_value(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改自定义参数
        redis_config = [{"configName": "maxmemory-policy", "configValue": "error-config-value"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message

    @pytest.mark.regression
    def test_modify_config_with_empty_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = None
        redis_config = [{"configName": "maxmemory-policy", "configValue": "volatile-random"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_modify_config_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = "redis-error"
        redis_config = [{"configName": "maxmemory-policy", "configValue": "volatile-random"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_modify_config_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 修改自定义参数
        space_id = instance_data["deleted_space"]
        redis_config = [{"configName": "maxmemory-policy", "configValue": "volatile-random"}]
        error = modify_config_step(redis_cap, space_id, redis_config)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
