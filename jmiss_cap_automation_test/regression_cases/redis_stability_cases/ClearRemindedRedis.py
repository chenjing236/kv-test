# -*- coding: utf-8 -*-
import time

from BasicTestCase import *
from steps.RedisClusterOperationSteps import query_filter_cache_clusters_step, delete_redis_instance_step

logger_info = logging.getLogger(__name__)

def clear_reminded_redis(redis_cap, instance_data):
    # 清除残留redis实例
    clusters = query_filter_cache_clusters_step(redis_cap, {"filterName": instance_data["create_cache_cluster"]["spaceName"], "filterSpaceType": 1})
    if clusters is not None:
        for cluster in clusters:
            delete_redis_instance_step(redis_cap, cluster["spaceId"])
            time.sleep(2)
    logger_info.info("[STEP] Clear Reminded Redis have Finished!")