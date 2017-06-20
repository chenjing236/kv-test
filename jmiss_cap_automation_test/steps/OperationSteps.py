# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import logging
import time

from business_function.MongoCap import *
from business_function.Cap import *

logger_info = logging.getLogger(__name__)

# 运营系统删除资源
def delete_resource_step(config, instance_data, http_client, resource_id, resource_type):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.delete_resource(resource_id, resource_type)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to delete the mongo instance, error message is [%s]",  error_msg)
        assert False, "[ERROR] It is failed to delete the mongo instance, error message is {2}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id

# 运营系统删除未过期资源
def delete_no_overdue_resource_step(config, instance_data, http_client, resource_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.delete_no_overdue_resource(resource_id, instance_data["operation_data"]["resourceType"], instance_data["operation_data"]["sourceAuth"])
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to delete the no-overdue instance of the mongo, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to delete the no-overdue instance of the mongo, error message is {0}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id

def modify_user_visible_flavor_step(config, instance_data, http_client, flavor_info):
    cap = Cap(config, instance_data, httpClient)
    res_data = cap.modify_user_visible_flavor(flavor_info)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = json.dumps(res_data["message"]).decode('unicode-escape')
        logger_info.error("[ERROR] It is failed to change the flavor to enable/disable status, error message is [%s]", error_msg)
        assert False, "[ERROR] It is failed to change the flavor to enable /disable, error message is {0}".format(error_msg)
    request_id = res_data["requestId"]
    return request_id
