#!/usr/bin/python
# coding:utf-8

import httplib
import json


# 缓存云HTTP API
class HttpClient(object):
    def __init__(self, host, md5_pin, auth_token, version):
        self.host = host
        self.md5_pin = md5_pin
        self.auth_token = auth_token
        self.version = version

    def http_request(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}/{1}/{2}".format(self.version, self.md5_pin, uri), data, {"auth-Token": self.auth_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def to_json_string(self, args):
        return json.dumps(args)

    # 创建缓存云实例 create
    def create_cluster(self, create_args):
        data = self.to_json_string(create_args)
        return self.http_request("POST", "clusters", data)

    # 删除缓存云实例 delete
    def delete_cluster(self, space_id):
        return self.http_request("DELETE", "clusters/{0}".format(space_id))

    # 设置访问规则 set acl allow
    def set_acl(self, space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "allow"}
        return self.http_request("PUT", "acl", json.dumps(acl))

    # 删除访问规则 set acl deny
    def del_acl(self, space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "deny"}
        return self.http_request("PUT", "acl", json.dumps(acl))

    # 扩容/缩容操作 resize
    def resize_cluster(self, space_id, zoneId, capacity):
        data = {"zoneId": zoneId, "capacity": capacity}
        return self.http_request("PUT", "resize/{0}".format(space_id), json.dumps(data))

    # 获取当前用户创建的缓存云实例列表 get clusters
    def get_clusters(self):
        return self.http_request("GET", "clusters")

    # 获取缓存云实例详情 get cluster
    def get_cluster(self, space_id):
        return self.http_request("GET", "clusters/{0}".format(space_id))

    # 获取ACL访问规则 get acl
    def get_acl(self, space_id):
        return self.http_request("GET", "acl/{0}".format(space_id))

    # update password
    def reset_password(self, space_id, password):
        data = {"password": password}
        return self.http_request("PUT", "updatepassword/{0}".format(space_id), json.dumps(data))

    # 获取操作结果 operation result
    def get_operation_result(self, space_id, operation_id):
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}".format(space_id, operation_id))

    # 设置系统级访问规则 set system acl
    def set_system_acl(self, space_id, enable):
        target = {"target": [space_id], "enable": enable}
        return self.http_request("PUT", "sysacl", json.dumps(target))

    # 修改基本信息 update meta
    def update_meta(self, space_id, space_name, remarks):
        data = {"spaceName": space_name, "remarks": remarks}
        return self.http_request("PUT", "updatemeta/{0}".format(space_id), json.dumps(data))

    # 获取资源实时信息 realtime info
    def get_realtime_info(self, space_id):
        return self.http_request("GET", "realtimeinfo?spaceIds={0}".format(space_id))

    # 获取资源使用详情/监控数据 resource info
    def get_resource_info(self, space_id, period, frequency):
        return self.http_request("GET", "resourceinfo/{0}?period={1}&frequency={2}".format(space_id, period, frequency))

    # rebuild upgrade spaceId
    # rebuild repair spaceId
    # rebuild clone
