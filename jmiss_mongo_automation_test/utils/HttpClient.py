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
        hc.request(method, "/{0}".format("cc-server", action), data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close
        return status, headers, res_data

    # 获取nova agent服务
    def http_request_for_nova_agent(self, method, uri, nova_agent_host, data=None):
	hc = httplib.HTTPConnection(nova_agent_host)
        hc.request(method, "/container/{0}".format(uri), data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close
        return status, headers, res_data

    # 获取mongo agent的client
    def http_request_for_mongo_agent(self, method, mongo_agent_host, uri, data=None):
        hc = httplib.HTTPConnection(mongo_agent_host)
        hc.request(method, uri, data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close
	return status, headers, res_data

    # 获取mongo实例的container信息
    def get_container_info(self, nova_agent_host, nova_container_id):
	nova_agent = nova_agent_host + ":1024"
	return self.http_request_for_nova_agent("GET", "stats?name=nova-{0}".format(nova_container_id), nova_agent)

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
    def updatemeta_mongo_name(self, space_id, data):
        return self.http_request("PUT", "updatemeta/{0}".format(space_id), json.dumps(data))

    # 获取操作结果
    def get_operation_result(self, space_id, operation_id):
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}".format(space_id, operation_id))

    # 获取flavor的详细信息
    def get_flavor_detail_info(self, flavor_id):
        return self.http_request("GET", "flavordetail/{0}".format(flavor_id))

    # 获取flavor id
    def get_flavor_id(self, data):
	#return self.http_request("GET", "flavorid?cpu={0}&disk={1}&iops={2}&memory={3}&maxConn={4}".format(data["cpu"], data["disk"], data["iops"], data["memory"], data["maxconn"]))
	return self.http_request("GET", "flavorid?{0}".format(data))

    # 删除mongo实例
    def delete_mongo_instance(self, space_id):
        return self.http_request("DELETE", "clusters/{0}".format(space_id))

    # 获取mongo的拓扑结构
    def get_topology_of_mongo(self, space_id):
	return self.http_request("GET", "topology/{0}".format(space_id))

    # 获取mongo操作结果
    def get_results_of_operation(self, space_id, operation_id):
	return self.http_request("GET", "operation?spaceId={0}&operationId={1}".format(space_id, operation_id))

    # ping mongo的container是否存在
    def ping_container_of_mongo_instance(self, mongo_agent_host, container_id):
	uri = "/ping?dockerId={0}".format(container_id)
	return self.http_request_for_mongo_agent("GET", mongo_agent_host, uri)

    # 通过uds访问container获取拓扑结构
    def get_replic_info_from_container(self, mongo_agent_host, container_id):
	uri = "/rsstatus?dockerId={0}".format(container_id)
        return self.http_request_for_mongo_agent("GET", mongo_agent_host, uri)

    # 获取实时信息
    def get_real_time_info(self, space_id):
	return self.http_request("GET", "realtimeinfo?spaceIds={0}".format(space_id))

    # 获取监控信息
    def get_monitor_info(self, space_id, data):
	return self.http_request("GET", "resourceinfo/{0}".format(data))

    # 分页查询列表
    def get_clusters_by_page(self, data):
	return self.http_request("GET", "clustersByPage?{0}".format(data))
