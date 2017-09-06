# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.RedisClusterOperationSteps import query_filter_cache_clusters_step

logger_info = logging.getLogger(__name__)

# 查询详情列表
def query_filter_cache_cluster(redis_cap, resource_id):
    clusters = query_filter_cache_clusters_step(redis_cap, {})
    #for cluster in clusters:
     #   assert cluster["status"] != 102, "[ERROR] There is a cluster which status equals 102 in the cluster list"
      #  if cluster["spaceId"] != resource_id:
       #     clusters.remove(cluster)
    return clusters