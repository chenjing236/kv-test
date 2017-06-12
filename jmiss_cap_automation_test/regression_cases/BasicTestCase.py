# -*- coding: utf-8 -*- 

import pytest
import logging

info_logger = logging.getLogger(__name__)

# 创建redis实例
@pytest.fixture(scope="class")
def create_redis_instance(self, config, data, http_client):
    info_logger.info("[STEP] Create a Create an instance for redis, the instance consists of a master and a slave")
    request_id = create_an_instance_step(config, instance_data, http_client)
    # tear down 删除redis实例
    return request_id    
