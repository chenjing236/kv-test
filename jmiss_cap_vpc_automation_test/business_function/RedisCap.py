# coding:utf-8
import logging

info_logger = logging.getLogger(__name__)


# 缓存云Redis中间层类
class RedisCap(object):
    def __init__(self, config, instance_data, http_client):
        self.config = config
        self.instance_data = instance_data
        self.http_client = http_client

    # 创建单实例缓存云实例
    def create_instance(self):
        create_data = self.instance_data["redis_cluster_info"]
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"],
                "quantity": create_data["quantity"], "remarks": create_data["remarks"],
                "password": create_data["password"], "itemType": create_data["itemType"],
                "networkOperator": create_data["networkOperator"], "chargeMode": create_data["chargeMode"],
                "chargeDuration": create_data["chargeDuration"], "chargeUnit": create_data["chargeUnit"],
                "promotionType": create_data["promotionType"], "masterAvailableZone": create_data["masterAvailableZone"],
                "slaverAvailableZone": create_data["slaverAvailableZone"], "cpu": create_data["flavor"]["cpu"],
                "disk": create_data["flavor"]["disk"], "maxConn": create_data["flavor"]["maxConn"], "net": create_data["flavor"]["net"],
                "memory": create_data["flavor"]["memory"], "vpcId": create_data["vpcId"], "subnetId": create_data["subnetId"]}
        status, headers, res_data = self.http_client.create_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 创建包年包月缓存云实例,跳过支付页面
    def create_month_instance(self):
        create_data = self.instance_data["redis_cluster_info"]
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceName": create_data["spaceName"], "spaceType": create_data["spaceType"],
                "quantity": create_data["quantity"], "remarks": create_data["remarks"],
                "password": create_data["password"], "itemType": create_data["itemType"],
                "networkOperator": create_data["networkOperator"], "chargeMode": create_data["chargeMode_month"],
                "chargeDuration": create_data["chargeDuration"], "chargeUnit": create_data["chargeUnit"],
                "promotionType": create_data["promotionType"],
                "masterAvailableZone": create_data["masterAvailableZone"],
                "slaverAvailableZone": create_data["slaverAvailableZone"],
                "cpu": create_data["flavor"]["cpu"], "disk": create_data["flavor"]["disk"],
                "maxConn": create_data["flavor"]["maxConn"], "net": create_data["flavor"]["net"],
                "memory": create_data["flavor"]["memory"], "vpcId": create_data["vpcId"], "subnetId": create_data["subnetId"],
                "source": create_data["source"]}
        status, headers, res_data = self.http_client.create_cache_cluster_with_new_payment(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, cluster_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id}
        status, headers, res_data = self.http_client.query_cache_cluster_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 根据订单查询云缓存实例详情
    def query_cache_cluster_detail_by_order(self, cluster_id, order_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id, "orderId": order_id}
        status, headers, res_data = self.http_client.query_cache_cluster_detail_by_order(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 根据过滤条件查云缓存实例列表
    def query_filter_cache_clusters(self, filter_data):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"]}
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
        if 'category' in filter_data:
            data["category"] = filter_data["category"]
        status, headers, res_data = self.http_client.query_filter_cache_clusters(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 更新缓存云实例基本信息
    def update_cache_cluster(self, space_id, update_data):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId": space_id}
        if "spaceName" in update_data:
            data["spaceName"] = update_data["spaceName"]
        if "remarks" in update_data:
            data["remarks"] = update_data["remarks"]
        if "password" in update_data:
            data["password"] = update_data["password"]
        if "mark" in update_data:
            data["mark"] = update_data["mark"]
        status, headers, res_data = self.http_client.update_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 批量删除云缓存实例
    def delete_cache_clusters(self, cluster_ids):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterIds": cluster_ids}
        status, headers, res_data = self.http_client.delete_cache_clusters(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 删除云缓存实例
    def delete_cache_cluster(self, cluster_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "clusterId": cluster_id}
        status, headers, res_data = self.http_client.delete_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # redis扩容缩容
    def modify_cache_cluster(self, cluster_id, is_resize):
        common_data = self.instance_data["common_data"]
        create_data = self.instance_data["redis_cluster_info"]
        if is_resize == 1:
            memory = create_data["flavor_resize"]["memory"]
            cpu = create_data["flavor_resize"]["cpu"]
            disk = create_data["flavor_resize"]["disk"]
            max_conn = create_data["flavor_resize"]["maxConn"]
            net = create_data["flavor_resize"]["net"]
        else:
            memory = create_data["flavor_reduce"]["memory"]
            cpu = create_data["flavor_reduce"]["cpu"]
            disk = create_data["flavor_reduce"]["disk"]
            max_conn = create_data["flavor_reduce"]["maxConn"]
            net = create_data["flavor_reduce"]["net"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "spaceType": create_data["spaceType"], "spaceName": create_data["spaceName"],
                "quantity": create_data["quantity"], "itemType": create_data["itemType"],
                "networkOperator": create_data["networkOperator"], "chargeMode": create_data["chargeMode"],
                "promotionType": create_data["promotionType"], "memory": memory, "cpu": cpu, "disk": disk, "maxConn": max_conn,
                "net": net, "cacheClusterId": cluster_id}
        status, headers, res_data = self.http_client.modify_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 启动缓存云实例
    def start_cache_cluster(self, space_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId": space_id}
        status, headers, res_data = self.http_client.start_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 停服缓存云实例
    def stop_cache_cluster(self, space_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "spaceId": space_id}
        status, headers, res_data = self.http_client.stop_cache_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 查询flavor列表
    def query_flavors(self):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "type": "redis_cluster"}
        status, headers, res_data = self.http_client.query_flavors(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
