# -*- coding: utf-8 -*-
import json
import logging
from business_function.Container import *

info_logger = logging.getLogger(__name__)

#获取container的flavor信息
def get_flavor_info_from_container_step(config, instance_data, http_client, docker_client, container_instance):
    #通过docker inspect获取flavor信息
    container = Container(config, http_client, docker_client)
    container_info = container.get_container_info(container_instance["host_ip"], container_instance["docker_id"])
    return container_info

