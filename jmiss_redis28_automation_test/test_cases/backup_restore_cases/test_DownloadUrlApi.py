# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestDownloadUrlApi:
    @pytest.mark.regression
    def test_query_backup_url_ms(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "query_download_url"
            base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        else:
            base_id = ""
            for backup in backup_list:
                if backup["backupStatus"] == 2:
                    base_id = str(backup["baseId"])
                    break
        # 获取备份文件下载链接
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error is None
        assert len(download_urls) > 0
        assert download_urls[0]["link"] != ""

    @pytest.mark.regression
    def test_query_backup_url_cluster(self, config, instance_data, http_client, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
        cluster = Cluster(config, instance_data, http_client)
        # 查询备份列表，获取备份base_id
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id)
        if total_count == 0:
            file_name = "query_download_url"
            base_id, error = create_backup_step(redis_cap, cluster, space_id, file_name)
        else:
            base_id = ""
            for backup in backup_list:
                if backup["backupStatus"] == 2:
                    base_id = backup["baseId"]
                    break
        # 获取备份文件下载链接
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error is None
        # 集群备份下载链接为多条，包含多个链接
        assert len(download_urls) == 8
        assert download_urls[0]["link"] != ""

    @pytest.mark.regression
    def test_query_backup_url_with_empty_instance_id(self, config, instance_data, http_client, created_instance):
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
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_query_backup_url_with_error_instance_id(self, config, instance_data, http_client, created_instance):
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
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_backup_url_with_deleted_instance_id(self, config, instance_data, http_client, created_instance):
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
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_backup_url_with_empty_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        base_id = None
        # 执行恢复操作
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error is None
        assert len(download_urls) == 0

    @pytest.mark.regression
    def test_query_backup_url_with_error_base_id(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        base_id = "base-id-error"
        # 执行恢复操作
        download_urls, error = query_download_url_step(redis_cap, space_id, base_id)
        assert error is None
        assert len(download_urls) == 0
