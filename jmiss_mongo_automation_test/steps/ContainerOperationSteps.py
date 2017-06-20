# -*- coding: utf-8 -*-
import json
import logging
from business_function.Container import *

info_logger = logging.getLogger(__name__)

# 获取container的
def get_flavor_info_from_container_step(config, host_ip, container_id):
    info_logger.info("[INFO] Get the flavor info of the container")
    container = Container(config)
    container.get_disk_size_of_container(host_ip, container_id)
