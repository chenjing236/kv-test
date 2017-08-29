# coding:utf-8

from utils.RedisClient import *
from business_function.Cluster import *
from business_function.Container import *

import json
import time
import logging

logger_info = logging.getLogger(__name__)


# 创建一个缓存云实例，返回缓存云实例的space_id
def get_container_info_step(container, nova_agent_host, container_id):
    res_data = container.get_container_info(nova_agent_host, container_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_container_info is incorrect for the container {0}".format(container_id)
    return res_data["memInfo"]

