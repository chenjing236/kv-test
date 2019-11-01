#!/usr/bin/python
# coding:utf-8

import httplib
import json
import uuid
import logging
info_logger = logging.getLogger(__name__)


def uuid_for_request_id():
    return uuid.uuid1()


def to_json_string(args):
    return json.dumps(args)


class HttpClient(object):
    def __init__(self, host, md5_pin, auth_token, version, tenant_id, jcs_docker_host, user):
        self.host = host
        self.md5_pin = md5_pin
        self.auth_token = auth_token
        self.version = version
        self.tenant_id = tenant_id
        self.jcs_docker_host = jcs_docker_host
        self.user = user

    def http_request(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}/{1}/{2}".format(self.version, self.md5_pin, uri), data, {"auth-Token": self.auth_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def http_request_for_op(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}".format(uri), data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def http_request_for_agent(self, agent_host, method, uri, data=None):
        hc = httplib.HTTPConnection(agent_host)
        hc.request(method, "{0}".format(uri), data, {"Content-Type": "application/json", "Cache-Control": "no-cache"})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def http_request_for_jcs_docker(self, method, action, client_token, data=None):
        hc = httplib.HTTPConnection(self.jcs_docker_host)
        hc.request(method, "/api-server?Action={0}".format(action), data,
                   {"User-Id": self.tenant_id, "Content-Type": "application/json", "Client-Token": client_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    # JMISS接口

    # 获取缓存云实例详情 get cluster
    def get_cluster(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "clusters/{0}?requestId={1}".format(space_id, request_id))

    # 获取ACL访问规则 get acl
    def get_acl(self, space_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "acl/{0}?requestId={1}".format(space_id, request_id))

    # 获取操作结果 operation result
    def get_operation_result(self, space_id, operation_id):
        request_id = uuid_for_request_id()
        return self.http_request("GET", "operation?spaceId={0}&operationId={1}&requestId={2}".format(space_id, operation_id, request_id))

    # 设置访问规则 set acl allow
    def set_acl(self, space_id):
        acl = {"target": [space_id], "ips": [], "action": "allow"}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "acl?requestId={0}".format(request_id), json.dumps(acl))

    # 设置系统级访问规则 set system acl
    def set_system_acl(self, space_id, enable):
        target = {"target": [space_id], "enable": enable}
        request_id = uuid_for_request_id()
        return self.http_request("PUT", "sysacl?requestId={0}".format(request_id), json.dumps(target))

    # Jmiss 运维接口

    # web查询down az状态
    def op_get_cluster_info(self):
        return self.http_request_for_op("GET", "op/get_cluster_info")

    # sagent 接口
    def ping_ap_version(self, sagent_host, container_id, space_id):
        return self.http_request_for_agent(sagent_host, "GET", "/pingAp?dockerId={0}&spaceId={1}".format(container_id, space_id))

    # NOVA agent接口

    # get jcs docker info
    def get_container_info(self, jcs_agent_host, container_id):
        data = {"id": container_id}
        return self.http_request_for_agent(jcs_agent_host, "POST", "/jvirt-jcs-eye?Action=DescribeContainer", to_json_string(data))

    # NOVA 接口

    # delete jcs docker
    def delete_jcs_docker(self, container_id):
        client_token = uuid_for_request_id()
        data = {"instance_id": container_id}
        return self.http_request_for_jcs_docker("POST", "DeleteContainer", client_token, to_json_string(data))

    # stop jcs docker
    def stop_jcs_docker(self, container_id):
        client_token = uuid_for_request_id()
        data = {"instance_id": container_id}
        return self.http_request_for_jcs_docker("POST", "StopContainer", client_token, to_json_string(data))
