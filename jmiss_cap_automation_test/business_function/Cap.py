# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)

# user模块，billing模块，order模块，公共模块
class Cap:
    def __init__(self, conf_obj, http_client):
        self.data_center = conf_obj["data_center"]
        self.user = conf_obj["user"]
	self.account = conf_obj["account"]
	self.http_client = http_client

    # user模块，查看用户quota
    def query_user_quota(self, resource):
	status, headers, res_data = self.httpClient.query_user_quota(resource)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # user模块，修改已用配额接口

    # 订单支付
    def pay(self, bill_pay_args):
        status, headers, res_data = self.httpClient.pay(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
