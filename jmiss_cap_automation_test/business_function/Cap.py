# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)

# user模块，billing模块，order模块，公共模块
class Cap:
    def __init__(self, conf_obj, data_obj, http_client):
	self.conf_obj = conf_obj
	self.data_obj = data_obj
	self.http_client = http_client

    # user模块，查看用户quota
    def query_user_quota(self, resource):
	status, headers, res_data = self.httpClient.query_user_quota(resource)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # user模块，修改已用配额接口

    # billing模块，订单支付
    def pay(self, order_request_id):
	common_data = self.data_obj["common_data"]
	data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "orderRequestId":order_request_id}
	status, headers, res_data = self.httpClient.pay(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    def query_order_status(self, order_request):
        common_data = self.data_obj["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "orderRequest":order_request}
        status, headers, res_data = self.httpClient.query_order_status(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
