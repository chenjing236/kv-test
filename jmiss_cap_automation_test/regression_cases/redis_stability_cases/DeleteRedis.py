# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.RedisClusterOperationSteps import delete_redis_instance_step

logger_info = logging.getLogger(__name__)

def delete_redis(redis_cap, resource_id):
    info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
    delete_redis_instance_step(redis_cap, resource_id)
