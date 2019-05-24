# coding:utf-8
from BasicTestCase import *


class TestBackupCluster:
    @pytest.mark.test
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_backup(self, config, created_instance):
        # 创建缓存云实例，创建成功
        space_id, cluster, password = created_instance
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
        # 执行备份操作
        base_id = create_backup_step(cluster, space_id)
        # 查询备份列表，验证备份执行成功
        backups = query_backup_list_step(cluster, space_id, base_id)
        assert backups[0]["cacheInstanceId"] == space_id, info_logger.error("The spaceId [{0}] of backup list is wrong!".format(backups[0]["cacheInstanceId"]))
        assert backups[0]["backupStatus"] == 2, info_logger.error("The status [{0}] of backup is wrong!".format(backups[0]["status"]))
        assert backups[0]["baseId"] == base_id, info_logger.error("The base_id [{0}] of backup is wrong!".format(backups[0]["baseId"]))
        # todo: flush data
        # 使用备份文件进行恢复
        create_restore_step(cluster, space_id, base_id)
        # 查询详情接口，验证资源状态正确
        detail_info = get_detail_info_of_instance_step(cluster, space_id)
        assert detail_info["status"] == 100, info_logger.error("The status of space [{0}] is wrong after restore!".format(space_id))
        # 验证通过nlb访问实例
        accesser = Accesser(config)
        check_access_nlb_step(accesser, space_id, password)
