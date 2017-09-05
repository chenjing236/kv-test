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
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"],
                "quantity": create_data["quantity"], "remarks": create_data["remarks"],
                "password": create_data["password"], "itemType": create_data["itemType"],
                "networkOperator": create_data["networkOperator"], "chargeMode": create_data["chargeMode"],
                "chargeDuration": create_data["chargeDuration"], "chargeUnit": create_data["chargeUnit"],
                "promotionType": create_data["promotionType"], "memory": create_data["memory"],
                "source": create_data["source"]}
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

    #创建包年包月缓存云实例，跳过支付页面
    def create_month_instance_skip_pay(self):
        create_data = self.instance_data["create_cache_cluster"]
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"],
                "quantity": create_data["quantity"],"remarks": create_data["remarks"],
                "password": create_data["password"],"itemType":create_data["itemType"],
                "networkOperator":create_data["networkOperator"],"chargeMode":create_data["chargeMode"],
                "chargeDuration":create_data["chargeDuration"],"chargeUnit":create_data["chargeUnit"],
                "promotionType":create_data["promotionType"],"memory":create_data["memory"],
                "source":create_data["source"]}
        status, headers, res_data = self.httpClient.create_cache_cluster_skip_pay(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, cluster_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id}
        status, headers, res_data = self.httpClient.query_cache_cluster_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 根据订单查询云缓存实例详情
    def query_cache_cluster_detail_by_order(self, cluster_id, order_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id, "orderId":order_id}
        status, headers, res_data = self.httpClient.query_cache_cluster_detail_by_order(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 根据过滤条件查云缓存实例列表
    def query_filter_cache_clusters (self, filter_data):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"]}
        if "filterName" in filter_data:
            data["filterName"] = filter_data["filterName"]
        if "filterSpaceType" in filter_data:
            data["filterSpaceType"] = filter_data["filterSpaceType"]
        if "filterStatus" in filter_data:
            data["filterStatus"] = filter_data["filterStatus"]
        if "sortName" in filter_data:
            data["sortName"] = filter_data["sortName"]
        if "sortRule" in filter_data:
            data["sortRule"] = filter_data["sortRule"]
        if "pageSize" in filter_data:
            data["pageSize"] = filter_data["pageSize"]
        if "pageNum" in filter_data:
            data["pageNum"] = filter_data["pageNum"]
        if "category" in filter_data:
            data["category"] = filter_data["category"]
        status, headers, res_data = self.httpClient.query_filter_cache_clusters(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 更新缓存云实例基本信息
    def update_cache_cluster(self, space_id, update_data):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId":space_id}
        if "spaceName" in update_data:
            data["spaceName"] = update_data["spaceName"]
        if "remarks" in update_data:
            data["remarks"] = update_data["remarks"]
        if "password" in update_data:
            data["password"] = update_data["password"]
        if "mark" in update_data:
            data["mark"] = update_data["mark"]
        status, headers, res_data = self.httpClient.update_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 批量删除云缓存实例
    def delete_cache_clusters(self, cluster_ids):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterIds": cluster_ids}
        status, headers, res_data = self.httpClient.delete_cache_clusters(data)
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

    # 启动缓存云实例
    def start_cache_cluster(self, space_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId": space_id}
        status, headers, res_data = self.httpClient.start_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 停服缓存云实例
    def stop_cache_cluster(self, space_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId": space_id}
        status, headers, res_data = self.httpClient.stop_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 获取实时被使用内存信息
    def real_time_info_cache_cluster(self, space_ids):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceIds": space_ids}
        status, headers, res_data = self.httpClient.real_time_info_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询flavor列表
    def query_flavors(self):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "type": "redis_cluster"}
        status, headers, res_data = self.httpClient.query_flavors(data)
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

    # Operation-运营停服接口
    def stop_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "user": common_data["user"],
                "resourceId": cluster_id, "resourceType": "redis"}
        status, headers, res_data = self.httpClient.stop_resource(data, operation_data["sourceAuth"])
        print res_data
        # 对于不欠费不过期资源计费不支持停服操作，会返回错误
        if status != 500:
            assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # Operation-运营修改用户可见flavor
    def modify_user_visible_flavor(self, cpu, memory, disk, action_type):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "user": common_data["user"],
                "cpu": cpu, "memory": memory, "disk": disk, "actionType": action_type, "type": "redis_cluster"}
        status, headers, res_data = self.httpClient.modify_user_visible_flavor(data, operation_data["sourceAuth"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询折扣信息
    def query_lowest_discount(self, fee_type):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "feeType": fee_type, "serviceCode": "redis"}
        status, headers, res_data = self.httpClient.query_lowest_discount(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询redis变配价格
    def query_resize_cache_price(self, space_id, memory):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "redisId": space_id, "memory": memory}
        status, headers, res_data = self.httpClient.query_resize_cache_price(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data