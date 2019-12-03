# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestBackupListApi:
    @pytest.mark.regression
    def test_query_backup_list_with_base_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "query_backup_list"
            base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        else:
            base_id = backup_list[0]["baseId"]
        # 获取备份列表
        filter_data = {"baseId": str(base_id)}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None
        assert total_count == 1
        assert backup_list[0]["baseId"] == base_id

    @pytest.mark.regression
    def test_query_backup_list_with_time(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "query_backup_list"
            create_backup_step(redis_cap, instance, space_id, file_name)
        # 获取备份列表
        filter_data = {"startTime": (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "endTime": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None
        assert total_count >= 1

    @pytest.mark.regression
    def test_query_backup_list_with_page(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "query_backup_list"
            create_backup_step(redis_cap, instance, space_id, file_name)
        # 获取备份列表
        filter_data = {"pageNumber": 1,
                       "pageSize": 10}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None
        assert total_count >= 1

    @pytest.mark.regression
    def test_query_backup_list_with_empty_instance_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        space_id = None
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_query_backup_list_with_error_instance_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        space_id = "redis-error"
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_backup_list_with_deleted_instance_id(self, instance_data, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        space_id = instance_data["deleted_space"]
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_backup_list_with_empty_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        filter_data = {"baseId": None}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None

    @pytest.mark.regression
    def test_query_backup_list_with_error_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        filter_data = {"baseId": "base-id-error"}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert total_count == 0
        assert error is None

    @pytest.mark.regression
    def test_query_backup_list_with_page_number_equal_0(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        filter_data = {"pageNumber": 0,
                       "pageSize": 10}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "pageNumber" in error.message

    @pytest.mark.regression
    def test_query_backup_list_with_page_size_equal_0(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        filter_data = {"pageNumber": 1,
                       "pageSize": 0}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "pageSize" in error.message

    @pytest.mark.regression
    def test_query_backup_list_with_future_time(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 获取备份列表
        filter_data = {"startTime": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "endTime": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None
        assert total_count == 0
