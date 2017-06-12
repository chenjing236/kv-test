# coding:utf-8

import logging
from utils.HttpClient import *

info_logger = logging.getLogger(__name__)

#缓存云Redis中间层类
class RedisCap(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient

    # 创建单实例缓存云实例
    def create_instance(self):
	create_data = selef.data_obj["create_cache_cluster"]
        data = {"dataCenter": create_data["dataCenter"], "user": create_data["user"], "account": create_data["account"], "spaceName": create_data["spaceName"], "spaceType": create_data["spaceTyep"], "capacity": create_data["capacity"], "quantity": create_data["quantity"], "remarks": create_data["remarks"], "password":create_data["password"], "feeType":create_data["feeType"]}
        status, headers, res_data = self.httpClient.create_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, cluster_id):
        common_data = selef.data_obj["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId":cluster_id}
        status, headers, res_data = self.httpClient.query_cache_cluster_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 删除云缓存实例
    def delete_cache_cluster(self, cluster_id):
        common_data = selef.data_obj["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId":cluster_id}
        status, headers, res_data = self.httpClient.delete_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
