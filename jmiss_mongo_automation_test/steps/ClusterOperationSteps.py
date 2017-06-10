# encoding:utf-8

import json
import logging

logger_info = logging.getLogger(__name__)

#创建一个mongo实例，返回mongo实例的space_id
def create_mongo_instance_step(instance):
    res_data = instance.create_mongo_instance(instance.data_obj["vpc_id"], instance.data_obj["subnetId"])
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to create an instance of mongo, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of creating an instance is incorrect")
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    return space_id
