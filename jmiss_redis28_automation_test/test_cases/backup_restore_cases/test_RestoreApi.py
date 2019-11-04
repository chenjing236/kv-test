# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestRestoreApi:
    @pytest.mark.regression
    def test_restore_with_empty_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "restore_api_test"
            base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        else:
            base_id = ""
            for backup in backup_list:
                if backup["backupStatus"] == 2:
                    base_id = backup["baseId"]
                    break
        # 执行恢复操作
        space_id = None
        error = restore_step(redis_cap, space_id, base_id)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_restore_with_error_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "restore_api_test"
            base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        else:
            base_id = ""
            for backup in backup_list:
                if backup["backupStatus"] == 2:
                    base_id = backup["baseId"]
                    break
        # 执行恢复操作
        space_id = "redis-error"
        error = restore_step(redis_cap, space_id, base_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_restore_with_deleted_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "restore_api_test"
            base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        else:
            base_id = ""
            for backup in backup_list:
                if backup["backupStatus"] == 2:
                    base_id = backup["baseId"]
                    break
        # 执行恢复操作
        space_id = instance_data["deleted_space"]
        error = restore_step(redis_cap, space_id, base_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "instanceId" in error.message

    @pytest.mark.regression
    def test_restore_with_empty_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        base_id = None
        # 执行恢复操作
        error = restore_step(redis_cap, space_id, base_id)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"

    @pytest.mark.regression
    def test_restore_with_error_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        base_id = "base-id-error"
        # 执行恢复操作
        error = restore_step(redis_cap, space_id, base_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "baseId" in error.message
