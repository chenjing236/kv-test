# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestBackupRestore:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_backup_ms_and_restore(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # todo:
        # 查看redis详情，获取访问域名
        # cluster_detail, error = query_detail_step(redis_cap, space_id)
        # domain = cluster_detail["connectionDomain"]
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
        # 执行备份操作
        file_name = "backup_ms_and_restore"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        # 查询备份列表，验证备份执行成功
        filter_data = {"baseId": str(base_id)}
        total_count, backup_list, error = query_backup_list_step(redis_cap, space_id, filter_data)
        assert error is None
        assert total_count == 1
        assert backup_list[0]["baseId"] == base_id
        assert backup_list[0]["cacheInstanceId"] == space_id
        assert backup_list[0]["backupType"] == 1
        assert backup_list[0]["backupStatus"] == 2
        assert backup_list[0]["backupFileName"] == file_name
        assert backup_list[0]["backupSize"] >= 0
        assert backup_list[0]["backupDownloadURL"] == ""
        # todo: flush all data
        # 使用备份文件进行恢复
        error = restore_step(redis_cap, space_id, base_id)
        assert error is None
        # 查询详情接口，验证资源状态正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        # todo:
        # 验证通过nlb访问实例
        # check_access_domain_step(accesser, space_id, password)
