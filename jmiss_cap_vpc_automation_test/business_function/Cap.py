# -*- coding: utf-8 -*-
import sys
import logging
reload(sys)
# sys.setdefaultencoding('utf-8')

logger_info = logging.getLogger(__name__)


# user模块，billing模块，order模块，公共模块
class Cap(object):
    def __init__(self, config, instance_data, http_client):
        self.config = config
        self.instance_data = instance_data
        self.http_client = http_client

    # user模块，查看用户配额
    def query_user_quota(self, resource):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "resource": resource}
        status, headers, res_data = self.http_client.query_user_quota(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # order模块，查询订单状态
    def query_order_status(self, order_request):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"], "orderRequest": order_request}
        status, headers, res_data = self.http_client.query_order_status(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # order模块，查询订单详情
    def query_order_detail(self, order_request_id):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "orderRequestId": order_request_id}
        status, headers, res_data = self.http_client.query_order_detail(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统，删除资源
    def delete_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "user": common_data["user"],
                "resourceId": cluster_id, "resourceType": operation_data["resourceType"]}
        status, headers, res_data = self.http_client.delete_resource(data, operation_data["sourceAuth"])
        print res_data
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统，删除未过期资源
    def delete_no_overdue_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"],
                "account": common_data["account"],
                "resourceId": cluster_id, "resourceType": operation_data["resourceType"]}
        status, headers, res_data = self.http_client.delete_no_overdue_resource(data, operation_data["sourceAuth"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统，资源停服
    def stop_resource(self, cluster_id):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"],
                "user": common_data["user"],
                "resourceId": cluster_id, "resourceType": "redis"}
        status, headers, res_data = self.http_client.stop_resource(data, operation_data["sourceAuth"])
        # 对于不欠费不过期资源计费不支持停服操作，会返回错误
        if status != 500:
            assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统，修改用户可见flavor
    def modify_user_visible_flavor(self, cpu, memory, disk, net, max_conn, action_type):
        common_data = self.instance_data["common_data"]
        operation_data = self.instance_data["operation_data"]
        data = {"dataCenter": common_data["dataCenter"], "account": common_data["account"], "user": common_data["user"],
                "cpu": cpu, "memory": memory, "disk": disk, "maxConn": max_conn,
                "net": net, "actionType": action_type, "type": "redis_cluster"}
        status, headers, res_data = self.http_client.modify_user_visible_flavor(data, operation_data["sourceAuth"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 运营系统，修改用户已用配额
    def modify_used_quota(self, resource, used_quota):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "resource": resource, "usedQuota": used_quota, "note": ""}
        status, headers, res_data = self.http_client.modify_used_quota(data)
        assert status == 200, "[ERROR] HTTP Request is failed, error message is {0}".format(res_data["message"])
        return res_data

    # 运营系统，设置用户总配额
    def modify_total_quota(self, resource, quota):
        common_data = self.instance_data["common_data"]
        data = {"dataCenter": common_data["dataCenter"], "user": common_data["user"], "account": common_data["account"],
                "resource": resource, "quota": quota, "note": ""}
        status, headers, res_data = self.http_client.modify_total_quota(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
