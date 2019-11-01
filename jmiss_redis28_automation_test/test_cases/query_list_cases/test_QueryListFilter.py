# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryListFilter:
    @pytest.mark.regression
    def test_query_list_without_filter(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 设置过滤条件为空
        filter_data = {}
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        if total_count >= 10:
            assert len(cluster_list) == 10
        else:
            assert len(cluster_list) == total_count
        info_logger.info("Test query list without filter successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceId", "values": ["redis-error"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) == 0
        info_logger.info("Test query list with filter of error instance id successfully!")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_query_list_with_filter_of_right_instance_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        filter_data = {
            "filters": [{"name": "cacheInstanceId", "values": [str(space_id), "redis-error"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) == 1
        assert cluster_list[0]["cacheInstanceId"] == space_id
        info_logger.info("Test query list with filter of right instance id successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_name(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceName", "values": ["redis-error-name-err"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) == 0
        info_logger.info("Test query list with filter of error name id successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_right_name(self, instance_data, created_instance):
        space_id, redis_cap, password, accesser = created_instance
        filter_data = {
            "filters": [{"name": "cacheInstanceName", "values": [str(instance_data["cache_instance_name"])]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) > 0
        info_logger.info("Test query list with filter of right instance name successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_status(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceStatus", "values": ["error-status"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "Invalid cacheInstanceStatus" in error.message
        info_logger.info("Test query list with filter of error status successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_right_status(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceStatus", "values": ["running"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) > 0
        info_logger.info("Test query list with filter of right status successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_version(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "redisVersion", "values": ["1.0"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "Invalid redisVersion" in error.message
        info_logger.info("Test query list with filter of error redis version successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_right_version(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "redisVersion", "values": ["2.8"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) > 0
        info_logger.info("Test query list with filter of right redis version successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_instance_type(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceType", "values": ["type-error"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) >= 0
        info_logger.info("Test query list with filter of error instance type successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_right_instance_type(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "cacheInstanceType", "values": ["master-slave"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) > 0
        info_logger.info("Test query list with filter of right instance type successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_error_charge_mode(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "chargeMode", "values": ["charge-mode-error"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "Invalid chargeMode" in error.message
        info_logger.info("Test query list with filter of right charge mode successfully!")

    @pytest.mark.regression
    def test_query_list_with_filter_of_right_charge_mode(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        filter_data = {
            "filters": [{"name": "chargeMode", "values": ["postpaid_by_duration"]}]
        }
        # 查看redis列表，验证列表数据正确
        total_count, cluster_list, error = query_list_step(redis_cap, filter_data)
        assert error is None
        assert len(cluster_list) > 0
        info_logger.info("Test query list with filter of error charge mode successfully!")
