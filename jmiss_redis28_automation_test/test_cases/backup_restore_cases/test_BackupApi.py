# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestBackupApi:
    @pytest.mark.regression
    def test_backup_with_empty_instance_id(self, config, instance_data, http_client):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        space_id = None
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"

    @pytest.mark.regression
    def test_backup_with_error_instance_id(self, config, instance_data, http_client):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        space_id = "redis-error"
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_backup_with_deleted_instance_id(self, config, instance_data, http_client):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        space_id = instance_data["deleted_space"]
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_backup_with_101_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host, config)
        scaler_modify_space_step(scaler_client, space_id, 1, status=101)
        # 执行备份操作
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 409
        assert error.status == "State"
        assert "error" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_backup_with_200_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host, config)
        scaler_modify_space_step(scaler_client, space_id, 1, status=200)
        # 执行备份操作
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 409
        assert error.status == "State"
        assert "creating" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_backup_with_300_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host, config)
        scaler_modify_space_step(scaler_client, space_id, 1, status=300)
        # 执行备份操作
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 409
        assert error.status == "State"
        assert "resizing" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_backup_with_600_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host, config)
        scaler_modify_space_step(scaler_client, space_id, 1, status=600)
        # 执行备份操作
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 409
        assert error.status == "State"
        assert "deleting" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_backup_with_800_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host, config)
        scaler_modify_space_step(scaler_client, space_id, 1, status=800)
        # 执行备份操作
        file_name = "backup"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 409
        assert error.status == "State"
        assert "restoring" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_backup_with_empty_file_name(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = ""
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "fileName" in error.message

    @pytest.mark.regression
    def test_backup_with_1_byte_file_name(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "a"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error is None

    @pytest.mark.regression
    def test_backup_with_2_bytes_file_name(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "a" * 2
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error is None

    @pytest.mark.regression
    def test_backup_with_16_bytes_file_name(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "a" * 16
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error is None

    @pytest.mark.regression
    def test_backup_with_file_name_longer_than_16(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "a" * 17
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error is None

    @pytest.mark.regression
    def test_backup_with_file_name_contain_special_symbol(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "backup@"
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "fileName" in error.message

    @pytest.mark.regression
    def test_backup_with_empty_backup_type(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "backup"
        backup_type = None
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name, backup_type=backup_type)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupType" in error.message

    @pytest.mark.regression
    def test_backup_with_backup_type_equal_1(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "backup"
        backup_type = 1
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name, backup_type=backup_type)
        assert error is None

    @pytest.mark.regression
    def test_backup_with_backup_type_equal_2(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "backup"
        backup_type = 2
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name, backup_type=backup_type)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupType" in error.message

    @pytest.mark.regression
    def test_backup_with_backup_type_equal_0(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 执行备份操作
        file_name = "backup"
        backup_type = 0
        base_id, error = create_backup_step(redis_cap, instance, space_id, file_name, backup_type=backup_type)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "backupType" in error.message
