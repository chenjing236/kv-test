# -*- coding: utf-8 -*- 


from BasicTestCase import *


class TestSmokeCasesForRedisCap:
    @pytest.mark.smoke
    def test_create_an_instance(self, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))

    @pytest.mark.smoke
    def test_query_filter_cache_clusters(self, create_redis_instance, create_redis_month_instance_with_new_payment):
        info_logger.info("[Scenario] Test queryFilterCacheClusters")
        # 创建按配置云缓存实例1，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 创建包年包月云缓存实例2，支付成功，验证资源状态为100
        redis_cap_month, cap_month, request_id_for_redis_month, resource_id_month = create_redis_month_instance_with_new_payment
        # 调用过滤条件查询列表接口，不添加过滤条件，查询成功
        filter_data = {}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        for cluster in clusters:
            info_logger.info("[Scenario]queryFilterCacheClusters result with no filter:{0}".format(cluster))

        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=1，filterName，验证返回列表包含按配置实例1
        filter_data = {"filterStatus": "100", "category": "1","filterName": "test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(cluster)))
            assert "test" in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=1 is incorrect!"
            assert cluster["billingOrder"]["chargeMode"] == 1, "[ERROR] QueryFilterCacheCluster use filter category=6 is incorrect"

        # 调用过滤条件查询列表接口，添加过滤条件status=100，feeType=6，filterName，验证返回列表包含包年包月实例2
        filter_data = {"filterStatus": "100", "category": "3", "filterName": "test"}
        clusters = query_filter_cache_clusters_step(redis_cap, filter_data)
        info_logger.info("[Scenario] queryFilterCacheClusters result:{0}".format(json.dumps(clusters)))
        for cluster in clusters:
            assert "test" in cluster["name"], "[ERROR] QueryFilterCacheClusters use filter category=6 is correct!"
            assert cluster["billingOrder"]["chargeMode"] == 3, "[ERROR] QueryFilterCacheCluster use filter category=6 is incorrect"
        info_logger.info("[INFO] Test query filter cacheClusters successfully!")
    '''
    @pytest.mark.smoke
    def test_renew_month_redis(self, create_redis_instance):
        info_logger.info("[Scenario] Test delete no_over_due redis instance with operation")
        # 创建按配置计费redis资源，用于续费
        info_logger.info("[STEP] Create a redis cluster for resizing")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
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
    '''
    @pytest.mark.smoke
    def test_resize_an_instance(self, instance_data, create_redis_instance):
        info_logger.info("[Scenario] Start to resize redis cluster")
        # 创建redis实例用于扩容
        info_logger.info("[STEP] Create a redis cluster for resizing")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        #print resource_id
        info_logger.info("[INFO] Create redis cluster successfully, the resourceId is {0}".format(resource_id))
        # 查询资源capacity
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        capacity = int(cluster["capacity"])
        # 查询升降配尾款账单余额
        #info_logger.info("[STEP] Query redis resize final payment")
        #final_payment_price = query_config_redis_final_payment_step(cap, resource_id)
        #assert final_payment_price == capacity * 3.28, "[ERROR] The final payment price is wrong!"
        #info_logger.info( "[INFO] Check redis resize final payment price successfully, the price is {0}".format(final_payment_price))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Resize redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
        # 调用支付接口
        # info_logger.info("[STEP] Pay for resize order")
        # pay_for_redis_instance_step(cap, request_id_resize)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query resize order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Redis resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(
            instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"
        info_logger.info("[INFO] Test redis cluster resize successfully!")

    @pytest.mark.smoke
    def test_reduce_an_instance(self, instance_data, create_redis_instance):
        info_logger.info("[Scenario] Start to reduce redis cluster")
        # 创建redis实例用于缩容
        info_logger.info("[STEP] Create a redis cluster for reducing")
        redis_cap, cap, request_id_create, resource_id = create_redis_instance
        print resource_id
        info_logger.info("[INFO] Create redis cluster successfully, the resourceId is {0}".format(resource_id))
        # 查询资源capacity
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        capacity = int(cluster["capacity"])
        # 查询升降配尾款账单余额
        #info_logger.info("[STEP] Query redis reduce final payment")
        #final_payment_price = query_config_redis_final_payment_step(cap, resource_id)
        #assert final_payment_price == capacity * 3.28, "[ERROR] The final payment price is wrong!"
        #info_logger.info(
         #   "[INFO] Check redis reduce final payment price successfully, the price is {0}".format(final_payment_price))
        # 调用扩容接口(is_resize 1:resize,0:reduce)
        info_logger.info("[STEP] Reduce redis cluster")
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 0)
        # 调用支付接口
        # info_logger.info("[STEP] Pay for reduce order")
        # pay_for_redis_instance_step(cap, request_id_resize)
        # 查询订单状态，验证缩容成功
        info_logger.info("[STEP] Query reduce order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Reduce resize failed!"
        # 查询资源详情，验证缩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(
            instance_data["create_cache_cluster"]["reduce_capacity"]), "[ERROR] The info of redis reduced is wrong!"
        info_logger.info("[INFO] Test reduce cluster resize successfully!")