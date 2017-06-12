# -*- coding: utf-8 -*-

import json
import logging
from business_function.Flavor import *

#根据flavor信息获取flavor id
def get_flavorid_by_flavorinfo_step(instance_data, http_client):
    flavor = Flavor(instance_data, http_client)
    res_data = flavor.get_flavor_id_by_flavor_info(instance_data["mongo_1C_2M_4D_10E"])
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] There is no flavor in db for the flavor info, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of getting flavor id is failed")
        assert False, "[ERROR] Response of getting flavor id is failed"
    flavor_id = attach["flavorId"]
    return flavor_id
