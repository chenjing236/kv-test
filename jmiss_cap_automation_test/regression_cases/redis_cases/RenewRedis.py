# -*- coding: utf-8 -*- 

from BasicTestCase import *
from steps.BillingOperationSteps import *
from steps.RedisClusterOperationSteps import *

info_logger = logging.getLogger(__name__)


class TestRenewRedis:

    @pytest.mark.renew
    def test_renew_redis(self, config, instance_data, redis_http_client, cap_http_client):
        info_logger.info("[Scenario] Test Renew redis instance")
        # 创建按配置计费redis资源，用于续费
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        # 创建redis实例
        info_logger.info("[STEP] Create an instance for redis, the instance consists of a master and a slave")
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # 支付
        info_logger.info("[STEP] Pay for the create order of redis instance")
        pay_for_redis_instance_step(cap, request_id_for_redis)
        # 查询订单状态
        info_logger.info("[STEP] Query order status, check the status of order")
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        # 查询详情接口
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Create redis instance successfully, the resourceId is {0}".format(resource_id))

        # 调用查询计费订单接口，验证计费方式为按配置
        info_logger.info("[STEP] Query bill order, check the feeType is 1")
        fee_type = query_bill_order_step(cap, resource_id)
        assert fee_type == 1, "[ERROR] The feeType of the redis instance is wrong!"
        info_logger.info("[INFO] Check the feeType of the redis instance successfully, the feeType = {0}".format(fee_type))
        # 调用查询资源状态接口，验证资源为正常状态，可以进行续费
        info_logger.info("[STEP] Query resource status, check it's normal")
        statusByResourceIdResponseList = query_status_by_resource_id_step(cap, resource_id)
        assert len(statusByResourceIdResponseList) == 0, "[ERROR] The status of the redis is wrong for the list of resource status is not null"
        info_logger.info("[INFO] Check resource status successfully, the list of resource status is null")
        # 调用查询批量续费价格接口，验证价格正确
        info_logger.info("[STEP] Query renew price of the redis instance, check the price")
        price_renew = query_renew_prices_step(cap, resource_id, 601)
        info_logger.info("[INFO] The renew price of the redis instance is {0}".format(price_renew))
        # 调用批量续费接口进行续费
        info_logger.info("[STEP] Renew for the redis instance")
        request_id_renew = renew_billing_orders_step(cap, resource_id, 601)
        # 调用支付接口进行支付
        info_logger.info("[STEP] Pay for the renew order of the redis instance")
        pay_for_redis_instance_step(cap, request_id_renew)
        # 查询订单状态，验证续费成功
        info_logger.info("[STEP] Query order status until renew over")
        success, resource_id = query_order_status_step(cap, request_id_renew)
        assert success == 1, "[ERROR] Renew redis failed!"
        # 调用查询计费订单接口，验证计费方式为包年包月
        info_logger.info("[STEP] Query bill order, check the feeType is 601")
        fee_type = query_bill_order_step(cap, resource_id)
        assert fee_type == 601, "[ERROR] The feeType of the redis instance is wrong!"
        info_logger.info("[INFO] Check the feeType of the redis instance successfully, the feeType = {0}".format(fee_type))
        # 调用运营删除未过期资源接口，删除redis资源
        info_logger.info("[STEP] Delete the redis instance with operation")
        request_id_delete = delete_no_overdue_resource_step(redis_cap, resource_id)
        print request_id_delete
        # 调用查询订单状态接口，验证资源删除成功
        info_logger.info("[STEP] Query delete order status, check the instance is deleted")
        success, resource_id = query_order_status_step(cap, request_id_delete)
        assert success == 1, "[ERROR] Delete redis instance with operation failed!"
        info_logger.info("[INFO] Test renew redis instance successfully!")

    @pytest.mark.renew
    def test_renew_month_redis(self, create_redis_month_instance):
        info_logger.info("[Scenario] Test delete no_over_due redis instance with operation")
        # 创建按配置计费redis资源，用于续费
        info_logger.info("[STEP] Create a redis cluster for resizing")
        redis_cap, cap, request_id_create, resource_id = create_redis_month_instance
        info_logger.info("[INFO] Create redis cluster successfully, the resourceId is {0}".format(resource_id))
        # 调用查询计费订单接口，验证计费方式为按配置
        info_logger.info("[STEP] Query bill order, check the feeType is 1")
        fee_type = query_bill_order_step(cap, resource_id)
        assert fee_type == 601, "[ERROR] The feeType of the redis instance is wrong!"
        info_logger.info("[INFO] Check the feeType of the redis instance successfully, the feeType = {0}".format(fee_type))
        # 调用查询资源状态接口，验证资源为正常状态，可以进行续费
        info_logger.info("[STEP] Query resource status, check it's normal")
        statusByResourceIdResponseList = query_status_by_resource_id_step(cap, resource_id)
        assert len(statusByResourceIdResponseList) == 0, "[ERROR] The status of the redis is wrong for the list of resource status is not null"
        info_logger.info("[INFO] Check resource status successfully, the list of resource status is null")
        # 调用查询批量续费价格接口，验证价格正确
        info_logger.info("[STEP] Query renew price of the redis instance, check the price")
        price_renew = query_renew_prices_step(cap, resource_id, 601)
        info_logger.info("[INFO] The renew price of the redis instance is {0}".format(price_renew))
        # 调用批量续费接口进行续费
        info_logger.info("[STEP] Renew for the redis instance")
        request_id_renew = renew_billing_orders_step(cap, resource_id, 601)
        # 调用支付接口进行支付
        info_logger.info("[STEP] Pay for the renew order of the redis instance")
        pay_for_redis_instance_step(cap, request_id_renew)
        # 查询订单状态，验证续费成功
        info_logger.info("[STEP] Query order status until renew over")
        success, resource_id = query_order_status_step(cap, request_id_renew)
        assert success == 1, "[ERROR] Renew redis failed!"
        # 调用查询计费订单接口，验证计费方式为包年包月
        info_logger.info("[STEP] Query bill order, check the feeType is 601")
        fee_type = query_bill_order_step(cap, resource_id)
        assert fee_type == 601, "[ERROR] The feeType of the redis instance is wrong!"
        info_logger.info("[INFO] Check the feeType of the redis instance successfully, the feeType = {0}".format(fee_type))
        info_logger.info("[INFO] Test renew redis instance successfully!")
