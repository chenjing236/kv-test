# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestBackupPolicyApi:
    @pytest.mark.regression
    def test_update_backup_policy_with_period(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查询备份策略
        backup_policy, error = query_backup_policy_step(redis_cap, space_id)
        # 修改备份策略
        backup_time_new = backup_policy["backupTime"]
        backup_period_new = "Sunday"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == backup_time_new
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_update_backup_policy_with_time(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查询备份策略
        backup_policy, error = query_backup_policy_step(redis_cap, space_id)
        # 修改备份策略
        backup_time_new = "05:00-06:00 +0800"
        backup_period_new = backup_policy["backupPeriod"]
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == backup_time_new
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_update_backup_policy_with_period_and_time(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "06:00-07:00 +0800"
        backup_period_new = "Saturday,"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == backup_time_new
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_update_backup_policy_with_empty_time(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = None
        backup_period_new = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupTime" in error.message

    @pytest.mark.regression
    def test_update_backup_policy_with_error_time(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "time-error"
        backup_period_new = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupTime" in error.message

    @pytest.mark.regression
    def test_update_backup_policy_with_other_time_zone(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "01:00-02:00 +0200"
        backup_period_new = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == "07:00-08:00 +0800"
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_update_backup_policy_with_empty_period(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "01:00-02:00 +0800"
        backup_period_new = None
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupPeriod" in error.message

    @pytest.mark.regression
    def test_update_backup_policy_with_error_period(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "01:00-02:00 +0800"
        backup_period_new = "period-error"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"

    @pytest.mark.regression
    def test_update_backup_policy_with_period_once_a_week(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "01:00-02:00 +0800"
        backup_period_new = "Monday,"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == backup_time_new
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_update_backup_policy_with_period_everyday(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 修改备份策略
        backup_time_new = "01:00-02:00 +0800"
        backup_period_new = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        error = modify_backup_policy_step(redis_cap, space_id, backup_time_new, backup_period_new)
        assert error is None
        # 查询备份策略
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert backup_policy_new["backupTime"] == backup_time_new
        assert backup_policy_new["backupPeriod"] == backup_period_new

    @pytest.mark.regression
    def test_query_backup_policy_with_empty_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查询备份策略
        space_id = None
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_query_backup_policy_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查询备份策略
        space_id = "redis-error"
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_query_backup_policy_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查询备份策略
        space_id = instance_data["deleted_space"]
        backup_policy_new, error = query_backup_policy_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
