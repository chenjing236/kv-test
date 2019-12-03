# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryClusterInfo:
    @pytest.mark.regression
    def test_query_clusterinfo_of_ms(self, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceType"] == 'master-slave'
        # 查看redis cluster info
        cluster_info, error = query_cluster_info_step(redis_cap, space_id)
        assert len(cluster_info["proxies"]) == 2
        assert len(cluster_info["shards"]) == 1
        info_logger.info("Test query cluster info of master-slave instance successfully!")

    @pytest.mark.regression
    def test_query_clusterinfo_of_cluster(self, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceType"] == 'cluster'
        # 查看redis cluster info
        cluster_info, error = query_cluster_info_step(redis_cap, space_id)
        assert len(cluster_info["proxies"]) > 2
        assert len(cluster_info["shards"]) > 1
        assert len(cluster_info["proxies"]) == len(cluster_info["shards"])
        info_logger.info("Test query cluster info of cluster successfully!")

    @pytest.mark.regression
    def test_query_clusterinfo_with_empty_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        cluster_info, error = query_cluster_info_step(redis_cap, "")
        assert error.code == 401
        assert error.status == "ACCESS_ERROR"
        info_logger.info("Test query cluster info with empty instance_id successfully!")

    @pytest.mark.regression
    def test_query_clusterinfo_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        cluster_info, error = query_cluster_info_step(redis_cap, "redis-error")
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test query cluster info with error instance_id successfully!")

    @pytest.mark.regression
    def test_query_clusterinfo_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        cluster_info, error = query_cluster_info_step(redis_cap, instance_data["deleted_space"])
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "has deleted" in error.message
        info_logger.info("Test query cluster info with deleted instance_id successfully!")

    # todo: query_clusterinfo_with_instance_id_of_others
