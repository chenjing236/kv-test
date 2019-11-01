# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryListPage:
    @pytest.mark.regression
    def test_query_list_of_first_page(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": 1,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 10:
            assert len(cluster_list) == 10
        else:
            assert len(cluster_list) == total_count
        info_logger.info("Test query list of first page successfully!")

    @pytest.mark.regression
    def test_query_list_of_second_page(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": 2,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 20:
            assert len(cluster_list) == 10
        elif total_count > 10:
            assert len(cluster_list) == total_count - 10
        else:
            assert len(cluster_list) == 0
        info_logger.info("Test query list of second page successfully!")

    @pytest.mark.regression
    def test_query_list_of_third_page(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": 3,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 30:
            assert len(cluster_list) == 10
        elif total_count > 20:
            assert len(cluster_list) == total_count - 20
        else:
            assert len(cluster_list) == 0
        info_logger.info("Test query list of third page successfully!")

    # todo: test_query_list_of_forth_page

    @pytest.mark.regression
    def test_query_list_of_larger_page_num(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": 100,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) == 0
        info_logger.info("Test query list of large pageNum successfully!")

    @pytest.mark.regression
    def test_query_list_of_zero_page(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": 0,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 10:
            assert len(cluster_list) == 10
        else:
            assert len(cluster_list) == total_count
        info_logger.info("Test query list of zero page successfully!")

    @pytest.mark.regression
    def test_query_list_of_negative_page(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "pageNumber": -1,
            "pageSize": 10
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert len(cluster_list) == 0
        info_logger.info("Test query list of negative page successfully!")
