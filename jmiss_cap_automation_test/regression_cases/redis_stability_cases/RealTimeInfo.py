# -*- coding: utf-8 -*-
import time
from BasicTestCase import *
from steps.RedisClusterOperationSteps import real_time_info_cache_cluster_step

logger_info = logging.getLogger(__name__)

#realtime info
def real_time_info(redis_cap,resource_id):
    request_id_realtime, infos = real_time_info_cache_cluster_step(redis_cap, resource_id)
    # print infos
    # assert infos[0]["memUsed"] != 0 and infos[0]["spaceId"] == resource_id
    for i in range(3):  # 重试三次，在三分钟周期内需取到realtimeinfo
        if infos is None:
            time.sleep(60)
            request_id_realtime, infos = real_time_info_cache_cluster_step(redis_cap, resource_id)
        else:
            break
    assert infos[0]["spaceId"] == resource_id