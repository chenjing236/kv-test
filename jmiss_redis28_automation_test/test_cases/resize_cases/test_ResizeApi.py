# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestResizeApi:
    @pytest.mark.regression
    def test_resize_ms_with_empty_instance_id(self, config, instance_data):
        # 扩容缓存云实例
        redis_cap = RedisCap(config, instance_data)
        space_id = ""
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test resize master-slave instance with empty instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_error_instance_id(self, config, instance_data):
        # 扩容缓存云实例
        redis_cap = RedisCap(config, instance_data)
        space_id = "redis-error"
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "not found" in error.message
        info_logger.info("Test resize master-slave instance with error instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_deleted_instance_id(self, config, instance_data):
        # 扩容缓存云实例
        redis_cap = RedisCap(config, instance_data)
        space_id = instance_data["deleted_space"]
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "has deleted" in error.message
        info_logger.info("Test resize master-slave instance with deleted instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_101_instance_id(self, config, instance_data, http_client, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=101)
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "FAILED_PRECONDITION"
        assert "ERROR" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
        info_logger.info("Test resize master-slave instance with error instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_200_instance_id(self, config, instance_data, http_client, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=200)
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "FAILED_PRECONDITION"
        assert "CREATING" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
        info_logger.info("Test resize master-slave instance with creating instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_300_instance_id(self, config, instance_data, http_client, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=300)
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "FAILED_PRECONDITION"
        assert "CHANGING" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
        info_logger.info("Test resize master-slave instance with changing instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_600_instance_id(self, config, instance_data, http_client, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=600)
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "FAILED_PRECONDITION"
        assert "DELETING" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
        info_logger.info("Test resize master-slave instance with deleting instance id successfully!")

    # todo: test_resize_ms_with_700_instance_id

    @pytest.mark.regression
    def test_resize_ms_with_800_instance_id(self, config, instance_data, http_client, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        instance = Cluster(config, instance_data, http_client)
        # 修改资源状态
        scaler_host = get_master_server_step(instance, "scaler")
        scaler_client = Scaler(scaler_host)
        scaler_modify_space_step(scaler_client, space_id, 1, status=800)
        cache_instance_class_resize = instance_data["cache_instance_class_resize"]
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "FAILED_PRECONDITION"
        assert "RESTORING" in error.message
        scaler_modify_space_step(scaler_client, space_id, 1, status=100)
        info_logger.info("Test resize master-slave instance with restoring instance id successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_empty_instance_class(self, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        cache_instance_class_resize = ""
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "cacheInstanceClass" in error.message
        info_logger.info("Test resize master-slave instance with empty instance class successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_error_instance_class(self, created_instance):
        # 扩容缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        cache_instance_class_resize = "error-flavor-id"
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "not found" in error.message
        info_logger.info("Test resize master-slave instance with error instance class successfully!")

    @pytest.mark.regression
    def test_resize_ms_with_same_instance_class(self, created_instance):
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_class = cluster_detail["cacheInstanceClass"]
        # 扩容缓存云实例
        cache_instance_class_resize = cache_instance_class
        error = resize_step(redis_cap, space_id, cache_instance_class_resize)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "same" in error.message
        info_logger.info("Test resize master-slave instance with the same instance class successfully!")
