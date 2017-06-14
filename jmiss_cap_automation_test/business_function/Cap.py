# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)


# user模块，billing模块，order模块，公共模块
class Cap(object):
    def __init__(self, config, instance_data, httpClient):
        self.config = config
        self.instance_data = instance_data
        self.httpClient = httpClient

    # user模块，查看用户quota
    def query_user_quota(self, resource):
        status, headers, res_data = self.httpClient.query_user_quota(resource)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # user模块，修改已用配额接口

    # billing模块，订单支付
    def pay(self, order_request_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "orderRequestId": order_request_id}
        status, headers, res_data = self.httpClient.pay(data)
        if status == 403 and res_data["code"] == 'OverAge':
            assert False, "[ERROR] 用户此地域没有配额！！！"
        assert status == 200, "[ERROR] HTTP Request is failed, error message is {0}".format(res_data["message"])
        return res_data

    # order模块，查询订单状态
    def query_order_status(self, order_request):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "orderRequest":order_request}
        status, headers, res_data = self.httpClient.query_order_status(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # order模块，查询订单详情
    def query_order_detail(self, order_request_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "orderRequestId": order_request_id}
        status, headers, res_data = self.httpClient.query_order_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，查询redis升降配尾款账单余额
    def query_config_redis_final_payment(self, redis_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "redisId": redis_id}
        status, headers, res_data = self.httpClient.query_config_redis_final_payment(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，查询redis资源价格
    def query_cache_price(self, memory, spaceType, feeType):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "memory": memory, "spaceType": spaceType, "feeType": feeType, "region": common_data["dataCenter"]}
        status, headers, res_data = self.httpClient.query_cache_price(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，批量查询redis续费价格
    def query_renew_prices(self, resourceId, feeType):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "feeType": feeType, "res": [{"resourceId": resourceId, "resourceType": "redis", "dataCenter": common_data["dataCenter"]}]}
        status, headers, res_data = self.httpClient.query_renew_prices(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，查询计费订单
    def query_bill_order(self, resourceId):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "resourceId": resourceId, "resourceType": "redis"}
        status, headers, res_data = self.httpClient.query_bill_order(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，根据resourceId查询资源状态--续费使用
    def query_status_by_resource_id(self, resourceId):
        common_data = self.instance_data["common_data"]
        create_data = self.instance_data["create_cache_cluster"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "statusByResourceIdResponseList": [{"resourceId": resourceId, "resourceName": create_data["spaceName"], "resourceType": "redis", "dataCenter": common_data["dataCenter"]}], "feeType": 1}
        status, headers, res_data = self.httpClient.query_status_by_resource_id(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，批量续费
    def renew_billing_orders(self, resourceId, feeType):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "feeType": feeType,
                "RenewBillingOrders": [{"resourceId": resourceId, "resourceType": "redis", "expireDateAfterRenew": ""}]}
        status, headers, res_data = self.httpClient.renew_billing_orders(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
