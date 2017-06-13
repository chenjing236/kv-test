# coding:utf-8

import logging
from utils.HttpClient import *

info_logger = logging.getLogger(__name__)

#缓存云Mongo中间层类
class MongoCap(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient

    # 创建mongo实例
    def create_instance(self):
	create_data = selef.data_obj["create_mongo_db"]
        data = {"dataCenter": create_data["dataCenter"], "user": create_data["user"], "account": create_data["account"], "cpu": create_data["cpu"], "memory":create_data["memory"], "maxLink":create_data["maxLink"], "ipos":create_data["ipos"], "dbType":create_data["dbType"], "netType":create_data["netType"], "routerId":create_data["routerId"], "subnetId":create_data["subnetId"], "dbVersion":create_data["dbVersion"], "routerName":create_data["routerName"], "subnetName":create_data["subnetName"], "feeType":create_data["feeType"], "disk":create_data["disk"], "password":create_data["password"]}
        status, headers, res_data = self.httpClient.create_mongo_db(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
