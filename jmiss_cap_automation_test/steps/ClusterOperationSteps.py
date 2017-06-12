# -*- coding: utf-8 -*- 

import json
import logging
import time

logger_info = logging.getLogger(__name__)

#创建一个mongo实例，返回mongo实例的space_id
def create_mongo_instance_step(config, instance_data, http_client):
    logger_info.info("========")
