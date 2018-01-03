# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.CapOperationSteps import *
from steps.RedisClusterOperationSteps import *


class TestOperationDeleteRedis:

    @pytest.mark.delete
    def test_operation_delete_redis(self, config, instance_data, redis_http_client, cap_http_client):
        info_logger.info("[Scenario] Test delete redis instance with operation")
        # 创建按配置计费redis资源，用于运营接口删除
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        # 创建redis实例
        info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create redis instance successfully, the resourceId is {0}".format(resource_id))
        # 调用运营删除接口删除资源
        info_logger.info("[STEP] Delete the redis instance with operation")
        request_id_delete = delete_resource_step(cap, resource_id)
        info_logger.info("[INFO] The request id of delete is {0}".format(request_id_delete))
        # 调用查询订单状态接口，验证资源删除成功
        # info_logger.info("[STEP] Query delete order status, check the instance is deleted")
        # success, resource_id = query_order_status_step(cap, request_id_delete)
        # assert success == 1, "[ERROR] Delete redis instance with operation failed!"
        info_logger.info("[INFO] Test delete redis instance with operation successfully!")

    @pytest.mark.delete
    def test_operation_delete_no_over_due_redis(self, config, instance_data, redis_http_client, cap_http_client):
        info_logger.info("[Scenario] Test delete no_over_due redis instance with operation")
        # 创建包年包月redis资源，用于运营接口删除
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        # 创建redis实例
        info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
        request_id_for_redis = create_redis_month_instance_step(redis_cap)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create redis instance successfully, the resourceId is {0}".format(resource_id))
        # 调用运营删除接口删除资源
        info_logger.info("[STEP] Delete the redis instance with operation")
        request_id_delete = delete_no_overdue_resource_step(cap, resource_id)
        info_logger.info("[INFO] The request id of delete is {0}".format(request_id_delete))
        # 调用查询订单状态接口，验证资源删除成功
        # info_logger.info("[STEP] Query delete order status, check the instance is deleted")
        # success, resource_id = query_order_status_step(cap, request_id_delete)
        # assert success == 1, "[ERROR] Delete redis instance with operation failed!"
        info_logger.info("[INFO] Test delete redis instance with operation successfully!")
