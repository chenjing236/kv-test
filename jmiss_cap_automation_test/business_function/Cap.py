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
            assert status == 403, "[ERROR] There is no quota for the user in this region, error message is [{0}]".format(res_data["message"])
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

    # billing模块，查询mongo的价格
    def query_mongo_db_price(self, flavor_info):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "cpu":flavor_info["cpu"], "memory":flavor_info["memory"], "disk":flavor_info["disk"], "feeType":flavor_info["feeType"], "region":flavor_info["region"]}
        status, headers, res_data = self.httpClient.query_mongo_db_price(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # billing模块，查询mongo的折扣
    def query_mongo_db_discount(self, discount_info):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "serviceCode":discount_info["serviceCode"], "feeType":discount_info["feeType"]}
        status, headers, res_data = self.httpClient.query_mongo_db_discount(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统删除资源
    def delete_resource(self, resourceId, resourceType):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "resourceId": resourceId, "resourceType":resourceType}
        status, headers, res_data = self.httpClient.delete_resource(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统删除未过期资源
    def delete_no_overdue_resource(self, resource_id, resource_type, source_auth):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "resourceId": resource_id, "resourceType":resource_type}
        status, headers, res_data = self.httpClient.delete_no_overdue_resource(data, source_auth)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营修改用户可见flavor
    def modify_user_visible_flavor(self, flavor_info):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "type":flavor_info["type"], "cpu":flavor_info["cpu"], "memory":flavor_info["memory"], "actionType":flavor_info["actionType"]}
        status, headers, res_data = self.httpClient.delete_no_overdue_resource(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
