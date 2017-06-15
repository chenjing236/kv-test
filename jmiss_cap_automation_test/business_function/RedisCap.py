# coding:utf-8
import logging

info_logger = logging.getLogger(__name__)


# 缓存云Redis中间层类
class RedisCap(object):
    def __init__(self, config, instance_data, httpClient):
        self.config = config
        self.instance_data = instance_data
        self.httpClient = httpClient

    # 创建单实例缓存云实例
    def create_instance(self):
        create_data = self.instance_data["create_cache_cluster"]
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"], "capacity": create_data["capacity"], "quantity": create_data["quantity"], "remarks": create_data["remarks"], "password": create_data["password"], "feeType": create_data["feeType"]}
        status, headers, res_data = self.httpClient.create_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 创建包年包月缓存云实例
    def create_month_instance(self):
        create_data = self.instance_data["create_cache_cluster"]
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"],
                "capacity": create_data["capacity"], "quantity": create_data["quantity"],
                "remarks": create_data["remarks"], "password": create_data["password"],
                "feeType": create_data["feeType_month"]}
        status, headers, res_data = self.httpClient.create_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, cluster_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id}
        status, headers, res_data = self.httpClient.query_cache_cluster_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 删除云缓存实例
    def delete_cache_cluster(self, cluster_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id}
        status, headers, res_data = self.httpClient.delete_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # redis扩容缩容
    def modify_cache_cluster(self, cluster_id, is_resize):
        common_data = self.instance_data["common_data"]
        create_data = self.instance_data["create_cache_cluster"]
        if is_resize == 1:
            capacity = create_data["resize_capacity"]
        else:
            capacity = create_data["reduce_capacity"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "cacheClusterId": cluster_id, "spaceType": create_data["spaceType"], "capacity": capacity,
                "quantity": create_data["quantity"], "feeType": create_data["feeType"]}
        status, headers, res_data = self.httpClient.modify_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # Operation-运营删除接口
    def delete_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "user": common_data["user"],
                "resourceId": cluster_id, "resourceType": operation_data["resourceType"]}
        status, headers, res_data = self.httpClient.delete_resource(data, operation_data["sourceAuth"])
        print res_data
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # Operation-运营删除接口
    def delete_no_overdue_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"],
                "account": common_data["account"],
                "resourceId": cluster_id, "resourceType": operation_data["resourceType"]}
        status, headers, res_data = self.httpClient.delete_no_overdue_resource(data, operation_data["sourceAuth"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
