# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import logging
from business_function.Container import *

info_logger = logging.getLogger(__name__)

#获取container的flavor信息
def get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_instance):
    #通过docker inspect获取flavor信息
    container = Container(config, http_client, docker_client)
    container_info = container.get_container_info(container_instance)
    return container_info

#验证mongo的container的状态，即验证mongo的container是否存活
def ping_container_step(config, instance_data, http_client, docker_client, container_instance):
    container = Container(config, http_client, docker_client)
    res_data = container.ping_container(container_instance)
    code = res_data["code"]
    message = json.dumps(res_data["message"]).decode('unicode-escape')
    #assert code == 0, "[ERROR] The contianer of the mongo cannot be reached, error message is {0}".format(msg)
    is_alive="true"
    if "Success" != res_data["message"]:
	is_alive = "false"
    return is_alive

#通过mongo agent的uds获取mongo的拓扑结构
def get_replica_info_from_container(config, instance_data, http_client, docker_client, container_instance):
    container = Container(config, http_client, docker_client)
    res_data = container.get_replica_info_from_container(container_instance)
    code = res_data["code"]
    message = json.dumps(res_data["message"]).decode('unicode-escape')
    assert code == 0, "[ERROR] Cannot get the replica info from the container [{0}], error message is {1}".format(container_instance["docker_id"], msg)
    return res_data["data"]
