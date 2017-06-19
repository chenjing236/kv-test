# -*- coding: utf-8 -*-

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
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to renew billing orders [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to renew billing orders {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id

# 运营系统删除未过期资源
def delete_no_overdue_resource_step(config, instance_data, http_client, resource_id):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.delete_no_overdue_resource(resource_id, instance_data["operation_data"]["resourceType"], instance_data["operation_data"]["sourceAuth"])
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to renew billing orders [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to renew billing orders {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id

# 运营修改用户可见flavor
def modify_user_visible_flavor_step(config, instance_data, http_client, resource_id, resource_type):
    cap = Cap(config, instance_data, http_client)
    res_data = cap.modify_user_visible_flavor(resource_type)
    request_id = res_data["requestId"]
    if "code" in res_data:
        error_msg = res_data["message"]
        logger_info.error("[ERROR] It is failed to renew billing orders [%s], resource_id is [%s], error message is [%s]", request_id, resource_id, error_msg)
        assert False, "[ERROR] It is failed to renew billing orders {0}, resource_id is {1} error message is {2}".format(request_id, resource_id, error_msg)
    request_id = res_data["requestId"]
    return request_id
