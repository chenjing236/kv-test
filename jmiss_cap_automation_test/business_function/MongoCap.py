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

    # 创建mongo实例,类型为按配置
    def create_instance(self):
	create_data = self.data_obj["create_mongo_db"]
        data = {"dataCenter": create_data["dataCenter"], "account": create_data["account"], "cpu": create_data["cpu"], "memory":create_data["memory"], "maxLink":create_data["maxLink"], "iops":create_data["iops"], "dbType":create_data["dbType"], "netType":create_data["netType"], "routerId":create_data["routerId"], "subnetId":create_data["subnetId"], "dbVersion":create_data["dbVersion"], "routerName":create_data["routerName"], "subnetName":create_data["subnetName"], "feeType":create_data["feeType"], "disk":create_data["disk"], "password":create_data["password"]}
        status, headers, res_data = self.httpClient.create_mongo_db(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 创建mongo实例，类型为按包年包月
    def create_instance_with_yearly_fee(self):
        create_data = self.data_obj["create_mongo_db_with_yearly_fee"]
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

    # 批量删除mongo实例
    def delete_mongo_dbs(self, resource_ids):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceIds":resource_ids}
        status, headers, res_data = self.httpClient.delete_mongo_dbs(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 修改mongo资源的名称
    def modify_mongo_db_name(self, resource_id, space_name):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceId":resource_id, "spaceName":space_name}
        status, headers, res_data = self.httpClient.modify_mongo_db_name(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询flavor信息
    def query_flavors(self, type):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "type":type}
        status, headers, res_data = self.httpClient.query_flavors(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询mongo列表过滤
    def query_filter_mongo_dbs(self, mongo_db_name, page_num):
        common_data = self.data_obj["common_data"]
        query_data = self.data_obj["query_filter_mongo_list"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"] ,"filterName":mongo_db_name, "pageNum":page_num,"filterStatus":query_data["filterStatus"],"pageSize":query_data["pageSize"],"sortRule":query_data["sortRule"],"sortName":query_data["sortName"]}
        status, headers, res_data = self.httpClient.query_filter_mongo_dbs(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询mongo列表
    def query_mongo_dbs(self):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"]}
        status, headers, res_data = self.httpClient.query_mongo_dbs(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询实时信息
    def query_mongo_realTimeInfo(self, resource_ids):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceIds":resource_ids}
        status, headers, res_data = self.httpClient.query_mongo_realTimeInfo(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询拓扑结构
    def query_mongo_topology(self, resource_id):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"], "spaceId":resource_id}
        status, headers, res_data = self.httpClient.query_mongo_topology(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询vpc列表
    def query_vpcs(self):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"]}
        status, headers, res_data = self.httpClient.query_vpcs(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询vpc子网列表
    def query_vpc_subnets(self,vpcId):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"],"vpcId":vpcId}
        status, headers, res_data = self.httpClient.query_vpc_subnets(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询vpc详情
    def query_vpc_detail(self,vpcId):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"],"id":vpcId}
        status, headers, res_data = self.httpClient.query_vpc_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询vpc子网详情
    def query_vpc_subnet_detail(self,subnetId):
        common_data = self.data_obj["common_data"]
        data = {"account":common_data["account"], "dataCenter":common_data["dataCenter"],"id":subnetId}
        status, headers, res_data = self.httpClient.query_vpc_subnet_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data