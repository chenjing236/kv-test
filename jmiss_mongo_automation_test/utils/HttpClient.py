#!/usr/bin/python
# coding:utf-8

import httplib
import json

#缓存云-MONGO的HTTP API
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

    def http_request_for_vpc(self, vpc_host):
        hc = httplib.HTTPConnection(vpc_host)

    def to_json_string(self, args):
        return json.dumps(args)

    #创建VPC
    def create_vpc(self, create_args):
        data = self.to_json_string(create_args)
        return self.http_request("POST", "clusters", data)

    # 创建mongo实例
    def create_mongo_instance(self, create_args):
        data = self.to_json_string(create_args)
        return self.http_request("POST", "clusters", data)

    # 删除mongo实例
    def delete_mongo_instance(self, space_id):
        return self.http_request("DELETE", "clusters/{0}".format(space_id))

    # 查看mongo实例详细信息
    def get_mongo_detail_info(self, space_id):
        return self.http_request("GET", "clusters/{0}".format(space_id))

    # 获取操作结果
    def get_operation_result(self, space_id, operation_id):
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}".format(space_id, operation_id))

    # 获取flavor的详细信息
    def get_flavor_detail_info(self, flavor_id):
        return self.http_request("GET", "flavordetail/{0}".format(flavor_id))