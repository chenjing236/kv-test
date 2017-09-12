# -*- coding: utf-8 -*-

from BasicTestCase import *
from redis_stability_cases.CraeteRedisWithNP import create_an_instance_with_NP
from redis_stability_cases.Verify import verify
import pytest
logger_info = logging.getLogger(__name__)
resource_id = ''
cluster_info = ''
redis_cap = ''
cap = ''
result = ["create.reason", "get_detail.reason", "get_list.reason", "update.reason",
                       "resize.reason", "reduce.reason", "delete.reason"]
result_error = ["create_error", "get_detail_error", "get_list_error", "update_error",
                             "resize_error", "reduce_error", "delete_error"]
index = 0
class TestStabilityOfCap:
    # 创建Redis实例
    def test_create_redis(self, create_an_instance_with_NP):
        global redis_cap
        global cap
        global resource_id
        global index
        redis_cap, cap,  resource_id = create_an_instance_with_NP
        index += 1

    # 查询详情
    def test_query_cache_cluster_detail(self):
        global redis_cap
        global resource_id
        global cluster_info
        global index
        info_logger.info("[STEP] Query redis instance detail, check the status of redis instance")
        billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster_info["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        index += 1

    #查询详情列表
    def test_query_filter_cache_cluster(self):
        global resource_id
        global cluster_info
        global redis_cap
        global index
        clusters = query_filter_cache_clusters_step(redis_cap, {})
        # 验证列表页信息与详情页一致
        verify(clusters,cluster_info, resource_id)
        index += 1

    # 更新实例信息
    def test_update_redis(self, instance_data):
        global resource_id
        global cluster_info
        global redis_cap
        global index
        space_name_update = instance_data["create_cache_cluster"]["spaceName"] + "_name_update"
        remarks_update = "remarks_update"
        mark = "updatebaseinfo"
        update_cache_cluster_step(redis_cap, resource_id, {"spaceName": space_name_update, "remarks": remarks_update, "mark": mark})
        # 查询详情接口验证更新信息的正确性
        space_name_update = instance_data["create_cache_cluster"]["spaceName"] + "_name_update"
        remarks_update = "remarks_update"
        billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster_info["name"] == space_name_update and cluster_info["remarks"] == remarks_update
        index += 1

    # 扩容
    def test_resize_to_expansion(self, instance_data):
        global resource_id
        global redis_cap
        global cap
        global index
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query resize order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Redis resize failed!"
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"
        index += 1
    # 缩容
    def test_resize_to_reduction(self, instance_data):
        global resource_id
        global redis_cap
        global cap
        global index
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 0)
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query reduce order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Reduce resize failed!"
        # 查询资源详情，验证扩容信息正确
        # info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["reduce_capacity"]), "[ERROR] The info of redis reduced is wrong!"
        index += 1
    '''
    # 删除资源
    # @pytest.mark.stability
    def test_delete_redis(self):
        global resource_id
        global redis_cap
        info_logger.info("[TEARDOWN] Delete the redis instance %s", resource_id)
        delete_redis_instance_step(redis_cap, resource_id)
    '''
    # 删除
    def test_delete_redis(self):
        global resource_id
        global redis_cap
        global index
        global result
        global result_error
        try:
            time.sleep(5)  # 创建失败情况等待中间层回滚
            if index != 0:
                delete_redis_instance_step(redis_cap, resource_id)
                # 如果删除执行成功，teardown时index还会加1
                if index == 6:
                    index += 1
        except Exception as e:
            # 删除前请求失败的情况
            index = 6
        i = 0
        while i < len(result):
            if i == index:
                print result[i] + ":1"
            else:
                print result[i] + ":0"
            i += 1
        # 输出总的监控项，正确为"0"，错误为"error_step"
        if index == 7:
            print "stab.redis.status:\"0\""
        else:
            print "stab.redis.status:\"{0}\"".format(result_error[index])


















