# coding:utf-8
import hashlib
import httplib
import json
from datetime import datetime
import logging
info_logger = logging.getLogger(__name__)


class Scaler:
    def __init__(self, host, conf_obj):
        self.scaler_host = host
        self.ark_token = conf_obj["ark_token"]

    def http_request(self, method, uri, data=None):
        headers = {"Content-Type": "application/json", "authtoken": self.ark_token}
        hc = httplib.HTTPConnection(self.scaler_host)
        hc.request(method, uri, data, headers)
        res = hc.getresponse()
        status = res.status
        data = res.read()
        # print data
        res_data = json.loads(data)
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    # 通过scaler modify_space接口修改space状态或者flavor_id
    # modify_type为1：修改space的状态status
    # modify_type为2：修改flavorId
    def scaler_modify_space(self, space_id, modify_type, status=0, flavor_id=""):
        uri = "/modify_space"
        if modify_type == 1:
            modify_data = {"spaceId": space_id, "type": 1, "status": status}
        else:
            modify_data = {"spaceId": space_id, "type": 2, "flavorId": flavor_id}
        status, headers, res_data = self.http_request("POST", uri, json.dumps(modify_data))
        assert status == 200
        assert res_data["Code"] == 0
        return
