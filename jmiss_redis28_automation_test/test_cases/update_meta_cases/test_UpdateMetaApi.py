# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestUpdateMetaApi:
    @pytest.mark.regression
    def test_update_meta_set_empty_name(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 修改资源name为空
        cache_instance_name_new = ""
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "empty" in error.message
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set empty name successfully!")

    @pytest.mark.regression
    def test_update_meta_with_name_shorter_than_2(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        # cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_name_new = "1"
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error is None
        # assert error.code == 400
        # assert error.status == "INVALID_ARGUMENT"
        # assert "empty" in error.message
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        # assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name_new
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set name shorter than 2 successfully!")

    @pytest.mark.regression
    def test_update_meta_with_name_equal_2(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源name
        cache_instance_name_new = "a" * 2
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name_new
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set name length equal 2 successfully!")

    @pytest.mark.regression
    def test_update_meta_with_name_equal_32(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源name
        cache_instance_name_new = "a" * 32
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name_new
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set name length equal 32 successfully!")

    @pytest.mark.regression
    def test_update_meta_with_name_longer_than_32(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_name_new = "a" * 33
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set name longer than 32 successfully!")

    @pytest.mark.regression
    def test_update_meta_with_name_include_special_signal(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_name_new = "test@"
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "invalid" in error.message
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set name include special signal successfully!")

    @pytest.mark.regression
    def test_update_meta_with_description_equal_256(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        # 只修改资源description
        cache_instance_description_new = "a" * 256
        error = update_meta_step(redis_cap, space_id, name=None, description=cache_instance_description_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description_new
        info_logger.info("Test update meta set description length equal 256 successfully!")

    @pytest.mark.regression
    def test_update_meta_with_description_longer_than_256(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_description_new = "a" * 257
        error = update_meta_step(redis_cap, space_id, name=None, description=cache_instance_description_new)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        assert "description" in error.message
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description
        info_logger.info("Test update meta set description longer than 256 successfully!")
