# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryListSort:
    @pytest.mark.regression
    def test_query_list_with_sort_of_empty_direction(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "sorts": [{"direction": "", "name": "createTime"}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "sort direction" in error.message
        info_logger.info("Test query list with sort of empty direction successfully!")

    @pytest.mark.regression
    def test_query_list_with_sort_of_createtime_asc(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "sorts": [{"direction": "asc", "name": "createTime"}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 2:
            assert cluster_list[0]["createTime"] < cluster_list[1]["createTime"]
        info_logger.info("Test query list with sort of create time asc successfully!")

    @pytest.mark.regression
    def test_query_list_with_sort_of_createtime_desc(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {
            "sorts": [{"direction": "desc", "name": "createTime"}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 2:
            assert cluster_list[0]["createTime"] > cluster_list[1]["createTime"]
        info_logger.info("Test query list with sort of create time desc successfully!")
