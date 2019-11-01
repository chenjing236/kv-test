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
