# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestUpdateMeta:
    @pytest.mark.regression
    def test_update_meta_set_name(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源name
        cache_instance_name_new = cache_instance_name + "_new"
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=None)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name_new
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description

    @pytest.mark.regression
    def test_update_meta_set_description(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_description_new = cache_instance_description + "_new"
        error = update_meta_step(redis_cap, space_id, name=None, description=cache_instance_description_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description_new

    @pytest.mark.newsmoke
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_update_meta_set_all(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        cache_instance_name = cluster_detail["cacheInstanceName"]
        cache_instance_description = cluster_detail["cacheInstanceDescription"]
        # 只修改资源description
        cache_instance_name_new = cache_instance_name + "_new"
        cache_instance_description_new = cache_instance_description + "_new"
        error = update_meta_step(redis_cap, space_id, name=cache_instance_name_new, description=cache_instance_description_new)
        assert error is None
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail_new, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail_new["cacheInstanceName"] == cache_instance_name_new
        assert cluster_detail_new["cacheInstanceDescription"] == cache_instance_description_new

        error = update_meta_step(redis_cap, space_id, name=cache_instance_name,
                                 description=cache_instance_description)
        if error is None:
            info_logger.info("Recover the instance %s Name and description successfully!" % space_id)
        else:
            info_logger.info("Failed to update the instance %s Name and description" % space_id)
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceName"] == cache_instance_name
        assert cluster_detail["cacheInstanceDescription"] == cache_instance_description
