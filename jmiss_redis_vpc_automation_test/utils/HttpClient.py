#!/usr/bin/python
# coding:utf-8

import httplib
import json
import uuid


def uuid_for_request_id():
    return uuid.uuid1()


def to_json_string(args):
    return json.dumps(args)


class HttpClient(object):
    def __init__(self, host, md5_pin, auth_token, version, tenant_id, nova_docker_host, nova_docker_token):
        self.host = host
        self.md5_pin = md5_pin
        self.auth_token = auth_token
        self.version = version
        self.tenant_id = tenant_id
        self.nova_docker_host = nova_docker_host
        self.nova_docker_token = nova_docker_token

    def http_request(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}/{1}/{2}".format(self.version, self.md5_pin, uri), data, {"auth-Token": self.auth_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def http_request_for_nova_agent(self, nova_agent_host, method, uri, data=None):
        hc = httplib.HTTPConnection(nova_agent_host)
        hc.request(method, "/{0}".format(uri), data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def http_request_for_nova_docker(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.nova_docker_host)
        hc.request(method, "/v2.1/{0}/servers/{1}".format(self.tenant_id, uri), data,
                   {"X-auth-Token": self.nova_docker_token, "User-Agent": "python-novaclient", "X-OpenStack-Nova-API-Version": 2.5})
        res = hc.getresponse()
        status = res.status
        hc.close()
        return status

    # JMISS接口

    # 创建缓存云实例 create
    def create_cluster(self, create_args):
        data = to_json_string(create_args)
        request_id = uuid_for_request_id()
        return self.http_request("POST", "clusters?requestId={0}".format(request_id), data)

    # 删除缓存云实例 delete
    def delete_cluster(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("DELETE", "clusters/{0}?requestId={1}".format(space_id, request_id))

    # 设置访问规则 set acl allow
    def set_acl(self, space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "allow"}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "acl?requestId={0}".format(request_id), json.dumps(acl))

    # 删除访问规则 set acl deny
    def del_acl(self, space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "deny"}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "acl?requestId={0}".format(request_id), json.dumps(acl))

    # 扩容/缩容操作 resize
    def resize_cluster(self, space_id, flavorId):
        data = {"flavorId": flavorId}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "resize/{0}?requestId={1}".format(space_id, request_id), json.dumps(data))

    # 获取当前用户创建的缓存云实例列表 get clusters
    def get_clusters(self):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "clusters?requestId={0}".format(request_id))

    # 使用过滤条件查询缓存云列表
    def get_filter_clusters(self, filters):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "clustersByPage?{0}&requestId={1}".format(filters, request_id))

    # 获取缓存云实例详情 get cluster
    def get_cluster(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "clusters/{0}?requestId={1}".format(space_id, request_id))

    # 获取ACL访问规则 get acl
    def get_acl(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "acl/{0}?requestId={1}".format(space_id, request_id))

    # update password
    def reset_password(self, space_id, password):
        data = {"password": password}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "updatepassword/{0}?requestId={1}".format(space_id, request_id), json.dumps(data))

    # 获取操作结果 operation result
    def get_operation_result(self, space_id, operation_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}&requestId={2}".format(space_id, operation_id, request_id))

    # 设置系统级访问规则 set system acl
    def set_system_acl(self, space_id, enable):
        target = {"target": [space_id], "enable": enable}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "sysacl?requestId={0}".format(request_id), json.dumps(target))

    # 修改基本信息 update meta
    def update_meta(self, space_id, space_name, remarks):
        if space_name == "":
            data = {"remarks": remarks}
        elif remarks == "":
            data = {"spaceName": space_name}
        else:
            data = {"spaceName": space_name, "remarks": remarks}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "updatemeta/{0}?requestId={1}".format(space_id, request_id), json.dumps(data))

    # 获取资源实时信息 realtime info
    def get_realtime_info(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "realtimeinfo?spaceIds={0}&requestId={1}".format(space_id, request_id))

    # 获取资源使用详情/监控数据 resource info
    def get_resource_info(self, space_id, period, frequency):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "resourceinfo/{0}?period={1}&frequency={2}&requestId={3}".format(space_id, period, frequency, request_id))

    # rebuild upgrade spaceId
    def rebuild_upgrade(self, space_id):
        request_id = uuid_for_request_id()
        data = {"srcSpaceId": space_id}
        return self.http_request("PUT", "upgrade?requestId={0}".format(request_id), json.dumps(data))

    # rebuild repair spaceId
    def rebuild_repair(self, space_id):
        request_id = uuid_for_request_id()
        data = {"srcSpaceId": space_id}
        return self.http_request("PUT", "repair?requestId={0}".format(request_id), json.dumps(data))

    # rebuild clone
    def rebuild_clone(self, clone_args):
        request_id = uuid_for_request_id()
        data = to_json_string(clone_args)
        return self.http_request("POST", "clone?requestId={0}".format(request_id), data)

    # query flavorId by config
    def query_flavor_id_by_config(self, flavor):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "flavorid?cpu={0}&disk={1}&memory={2}&maxConn{3}&net={4}&requestId={5}"
                                 .format(flavor["cpu"], flavor["disk"], flavor["memory"], flavor["maxConn"],
                                         flavor["net"], request_id))

    # query config by flavorId
    def query_config_by_flavor_id(self, flavor_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "flavordetail/{0}?requestId={1}".format(flavor_id, request_id))

    # NOVA 接口

    # get nova docker info
    def get_container_info(self, nova_agent_host, container_id):
        return self.http_request_for_nova_agent(nova_agent_host, "GET", "container/stats?name=nova-{0}".format(container_id))

    # delete nova docker
    def delete_nova_docker(self, container_id):
        return self.http_request_for_nova_docker("DELETE", container_id)

    # stop nova docker
    def stop_nova_docker(self, container_id):
        data = {"pause": None}
        return self.http_request_for_nova_docker("POST", container_id, json.dumps(data))
