#!/usr/bin/python
# coding:utf-8

import httplib
import json
import uuid


def to_json_string(args):
    return json.dumps(args)


class HttpClient(object):
    def __init__(self, host):
        self.host = host

    def http_request_for_scaler(self, method, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/vpc/upgrade", data)
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    # Scaler接口

    # 创建缓存云实例 create
    def upgrade_cluster(self, data):
        return self.http_request_for_scaler("POST", to_json_string(data))
