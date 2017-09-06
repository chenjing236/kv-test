# -*- coding: utf-8 -*-

from BasicTestCase import *
from steps.RedisClusterOperationSteps import update_cache_cluster_step, query_cache_cluster_detail_step


def update_redis(redis_cap, instance_data, resource_id):
    space_name_update = instance_data["create_cache_cluster"]["spaceName"] + "_name_update"
    remarks_update = "remarks_update"
    mark = "updatebaseinfo"
    update_cache_cluster_step(redis_cap, resource_id, {"spaceName": space_name_update, "remarks": remarks_update, "mark": mark})
    # 查询详情接口验证更新信息的正确性
    billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
    assert cluster_info["name"] == space_name_update and cluster_info["remarks"] == remarks_update