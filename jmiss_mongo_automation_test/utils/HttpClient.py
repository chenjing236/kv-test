#!/usr/bin/python
# -*- coding: utf-8 -*- 

import httplib
import json

#缓存云-MONGO的HTTP Client
class HttpClient(object):
    def __init__(self, host, cc_host, md5_pin, auth_token, version):
        self.host = host
        self.cc_host = cc_host
        self.md5_pin = md5_pin
        self.auth_token = auth_token
        self.version = version

    # mongo服务
    def http_request(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}/{1}/{2}".format(self.version, self.md5_pin, uri), data, {"auth-Token": self.auth_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    # 将json对象装换为string类型
    def to_json_string(self, args):
        return json.dumps(args)

    # cc服务
    def http_request_for_cc(self, action):
        hc = httplib.HTTPConnection(self.cc_host)
        hc.request(method, "/{0}?Action={1}".format("cc-server", action), data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close
        return status, headers, res_data

    # 创建VPC
    def create_vpc(self, create_vp_args):
        data = self.to_json_string(create_vp_args)
        return self.http_request_for_cc("POST", "CreateVpc", data)

    # 查看当前用户的VROUTERS
    def get_vrouters_of_vpc(self, vrouts_args):
        return self.http_request_for_cc("GET", "DescribeRouteTables", vrouts_args)

    # 创建子网
    def create_subnet(self, create_subnet_args):
        data = self.to_json_string(create_subnet_args)
        return self.http_request("POST", "clusters", data)

    # 创建mongo实例
    def create_mongo_instance(self, create_args):
        data = self.to_json_string(create_args)
        return self.http_request("POST", "clusters", data)

    # 查看mongo实例详细信息
    def get_mongo_detail_info(self, space_id):
        return self.http_request("GET", "clusters/{0}".format(space_id))

    # 获取mongo的实例列表
    def get_mongo_list(self):
        return self.http_request("GET", "clusters")

    # 查看mongo实例的副本集关系
    def get_mongo_replica(self, space_id):
        return self.http_request("GET", "topology/{0}".format(space_id))

    # 修改mongo实例名称
    def updatemeta_mongo_name(self, space_id, space_name):
        return self.http_request("PUT", "updatemeta/{0}".format(space_id))

    # 获取操作结果
    def get_operation_result(self, space_id, operation_id):
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}".format(space_id, operation_id))

    # 获取flavor的详细信息
    def get_flavor_detail_info(self, flavor_id):
        return self.http_request("GET", "flavordetail/{0}".format(flavor_id))

    # 删除mongo实例
    def delete_mongo_instance(self, space_id):
        return self.http_request("DELETE", "clusters/{0}".format(space_id))
