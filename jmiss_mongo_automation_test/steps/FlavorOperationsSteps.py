# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import logging
from business_function.Flavor import *

#根据flavor信息获取flavor id
def get_flavorid_by_flavorinfo_step(instance_data, http_client):
    flavor = Flavor(instance_data, http_client)
    res_data = flavor.get_flavor_id_by_flavor_info(instance_data["mongo_1C_2M_4D_10E"])
    code = res_data["code"]
    error_msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] There is no flavor in db for the flavor info, error message is {0}".format(error_msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of getting flavor id is failed")
        assert False, "[ERROR] Response of getting flavor id is failed"
    flavor_id = attach["flavorId"]
    return flavor_id

#根据flavor信息获取flavor id
def get_flavorid_by_flavor_info_step(instance_data, http_client, flavor_info_tag):
    flavor = Flavor(instance_data, http_client)
    res_data = flavor.get_flavor_id_by_flavor_info(instance_data[flavor_info_tag])
    code = res_data["code"]
    error_msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] There is no flavor in db for the flavor info, error message is {0}".format(error_msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of getting flavor id is failed")
        assert False, "[ERROR] Response of getting flavor id is failed"
    flavor_id = attach["flavorId"]
    return flavor_id

#根据flavor id获取flavor信息
def get_flavor_info_step(instance_data, http_client, flavor_id):
    flavor = Flavor(instance_data, http_client)
    res_data = flavor.get_flavor_info_by_flavor_id(flavor_id)
    code = res_data["code"]
    error_msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] There is no flavor in db for the flavor info, error message is {0}".format(error_msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of getting flavor id is failed")
        assert False, "[ERROR] Response of getting flavor id is failed"

    flavor_info=res_data["attach"]
    return flavor_info
