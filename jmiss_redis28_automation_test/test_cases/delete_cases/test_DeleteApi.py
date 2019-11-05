# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestDeleteApi:
    @pytest.mark.regression
    def test_delete_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 删除资源
        space_id = "redis-error"
        error = delete_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_delete_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 删除资源
        space_id = instance_data["deleted_space"]
        error = delete_step(redis_cap, space_id)
        assert error.code == 404
        assert error.status == "NOT_FOUND"

    @pytest.mark.regression
    def test_delete_with_creating_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=200)
        # 删除资源
        error = delete_step(redis_cap, space_id)
        assert error.code == 409
        assert error.status == "State"
        assert "creating" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_delete_with_changing_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=300)
        # 删除资源
        error = delete_step(redis_cap, space_id)
        assert error.code == 409
        assert error.status == "State"
        assert "changing" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)

    @pytest.mark.regression
    def test_delete_with_deleting_instance_id(self, config, instance_data, http_client, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=600)
        # 删除资源
        error = delete_step(redis_cap, space_id)
        assert error.code == 409
        assert error.status == "IN PROCESSING"
        assert "deleting" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
