# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryDetail:
    @pytest.mark.regression
    def test_query_detail_with_ms_instance_id(self, instance_data, created_instance):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_instance
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceName"] == instance_data["cache_instance_name"]
        assert cluster_detail["cacheInstanceDescription"] == instance_data["cache_instance_description"]
        assert cluster_detail["auth"] is True
        assert cluster_detail["vpcId"] == instance_data["vpc_id"]
        assert cluster_detail["subnetId"] == instance_data["subnet_id"]
        assert cluster_detail["redisVersion"] == "2.8"
        assert cluster_detail["charge"]["chargeStatus"] == "normal"
        # 验证为主从版
        assert cluster_detail["cacheInstanceType"] == 'master-slave'
        info_logger.info("Test query detail of master-slave instance successfully!")

    @pytest.mark.regression
    def test_query_detail_with_cluster_instance_id(self, instance_data, created_cluster):
        # 创建缓存云实例
        space_id, redis_cap, password, accesser = created_cluster
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceName"] == instance_data["cache_instance_name"]
        assert cluster_detail["cacheInstanceDescription"] == instance_data["cache_instance_description"]
        assert cluster_detail["auth"] is True
        assert cluster_detail["vpcId"] == instance_data["vpc_id"]
        assert cluster_detail["subnetId"] == instance_data["subnet_id"]
        assert cluster_detail["redisVersion"] == "2.8"
        assert cluster_detail["charge"]["chargeStatus"] == "normal"
        # 验证为集群版
        assert cluster_detail["cacheInstanceType"] == 'cluster'
        info_logger.info("Test query detail of cluster instance successfully!")

    @pytest.mark.regression
    def test_query_detail_with_empty_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        # space_id为空时，返回资源列表
        cluster_detail, error = query_detail_step(redis_cap, "")
        assert error is None
        assert len(cluster_detail) >= 0
        info_logger.info("Test query detail with empty instance_id successfully!")

    @pytest.mark.regression
    def test_query_detail_with_error_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        cluster_detail, error = query_detail_step(redis_cap, "redis-error")
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test query detail with error instance_id successfully!")

    @pytest.mark.regression
    def test_query_detail_with_deleted_instance_id(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查看redis cluster info
        cluster_detail, error = query_detail_step(redis_cap, instance_data["deleted_space"])
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert "has deleted" in error.message
        info_logger.info("Test query detail with deleted instance_id successfully!")

    # todo: query_detail_with_instance_id_of_others
