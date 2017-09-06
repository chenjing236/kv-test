# -*- coding: utf-8 -*-

from BasicTestCase import *

logger_info = logging.getLogger(__name__)

class StabilityOfCapCase:
    def __init__(self, config, instance_data, redis_http_client, cap_http_client):
        self.config = config
        self.instance_data = instance_data
        self.redis_http_client = redis_http_client
        self.cap_http_client = cap_http_client

    def 

