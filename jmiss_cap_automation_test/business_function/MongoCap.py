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
	create_data = self.data_obj["create_mongo_db"]
        data = {"dataCenter": create_data["dataCenter"], "account": create_data["account"], "cpu": create_data["cpu"], "memory":create_data["memory"], "maxLink":create_data["maxLink"], "iops":create_data["iops"], "dbType":create_data["dbType"], "netType":create_data["netType"], "routerId":create_data["routerId"], "subnetId":create_data["subnetId"], "dbVersion":create_data["dbVersion"], "routerName":create_data["routerName"], "subnetName":create_data["subnetName"], "feeType":create_data["feeType"], "disk":create_data["disk"], "password":create_data["password"]}
        status, headers, res_data = self.httpClient.create_mongo_db(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询monggo详情
    def query_mongo_db_detail(self, resource_id):
	common_data = self.data_obj["common_data"]
	data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceId":resource_id}
        status, headers, res_data = self.httpClient.query_mongo_db_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 删除mongo实例
    def delete_mongo_db(self, resource_id):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceId":resource_id}
        status, headers, res_data = self.httpClient.delete_mongo_db(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 修改mongo资源的名称
    def modify_mongo_db_name(self, resource_id, space_name):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceId":resource_id, "spaceName":space_name}
        status, headers, res_data = self.httpClient.modify_mongo_db_name(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
