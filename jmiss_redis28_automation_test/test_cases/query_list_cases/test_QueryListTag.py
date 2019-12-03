# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryListTag:
    @pytest.mark.regression
    def test_query_list_with_tag_set_value(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "tagFilters": [{"": ["test_value"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        info_logger.info("Test query list with tag only set value successfully!")

    @pytest.mark.regression
    def test_query_list_with_tag_set_key(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "tagFilters": [{"test_key": []}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        info_logger.info("Test query list with tag only set key successfully!")

    @pytest.mark.regression
    def test_query_list_with_tag_set_key_and_value(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "tagFilters": [{"test_key": ["test_value"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        info_logger.info("Test query list with tag set key and value successfully!")
