# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.RedisClusterOperationSteps import query_cache_cluster_detail_step

logger_info = logging.getLogger(__name__)

#查询详情接口
# print "[STEP] Query redis instance detail, check the status of redis instance"
def query_cache_cluster_detail(redis_cap, resource_id):
    info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
    billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster_info["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
    return cluster_info