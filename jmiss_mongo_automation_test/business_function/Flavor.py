# -*- coding: utf-8 -*- 

import logging

logger_info = logging.getLogger(__name__)

class Flavor(object):
    def __init__(self, data_obj, httpClient):
        self.data_obj = data_obj
        self.httpClient = httpClient

    # 根据flavor info获取flavor id
    def get_flavor_id_by_flavor_info(self, flavor_info):
	#assert flavor_info is None, "[ERROR] Flavor info is none"
	flavor_info="cpu={0}&disk={1}&iops={2}&memory={3}&maxConn={4}".format(self.data_obj["mongo_1C_2M_4D_10E"]["cpu"], self.data_obj["mongo_1C_2M_4D_10E"]["disk"], self.data_obj["mongo_1C_2M_4D_10E"]["iops"], self.data_obj["mongo_1C_2M_4D_10E"]["memory"], self.data_obj["mongo_1C_2M_4D_10E"]["maxconn"])
        status, headers, res_data = self.httpClient.get_flavor_id(flavor_info)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 根据flavor id获取flavor info
    def get_flavor_info_by_flavor_id(self, flavor_id):
        status, headers, res_data = self.httpClient.get_flavor_detail_info(flavor_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
