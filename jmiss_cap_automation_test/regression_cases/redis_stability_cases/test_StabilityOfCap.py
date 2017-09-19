# -*- coding: utf-8 -*-

from CreateRedisInstance import *
from QueryCacheClusterDetail import query_cache_cluster_detail
from QueryFilterCacheCluster import query_filter_cache_clusters
from UpdateRedis import update_redis
from Reduce import reduce_redis
from Resize import resize_redis
from VerifyRedis import verify_redis
from steps.RedisClusterOperationSteps import *
from BasicTestCase import *
from utils.HttpClient import *
from business_function.Cap import *
from business_function.RedisCap import *
import pytest
import json
import os
cap_http_client = ''
redis_http_client = ''
redis_cap = ''
cap = ""
resource_id = ''
cluster_info = {}
result = ["create.reason", "get_detail.reason", "get_list.reason", "update.reason",
                       "resize.reason", "reduce.reason", "delete.reason"]
result_error = ["create_error", "get_detail_error", "get_list_error", "update_error",
                             "resize_error", "reduce_error", "delete_error"]
index = {"create":1, "get_detail":1, "get_list":1, "update": 1, "resize": 1, "reduce": 1, "delete":1}
logger_info = logging.getLogger(__name__)

params = ["config\url"]
class TestStability:
    def setup_class(cls):
        logger_info.info("setup_class       class:%s" % cls.__name__)
        global cap_http_client, redis_http_client, cap, redis_cap
        url = os.path.join(os.getcwd(), params[0])
        file = json.load(open(url, 'r'))
        cls.config = file["config"]
        cls.instance_data = file["instance_data"]
        cls.config = json.load(open(cls.config, 'r'))
        cls.instance_data = json.load(open(cls.instance_data, 'r'))
        redis_http_client = RedisCapClient(cls.config["host"])
        cap_http_client = CapClient(cls.config["host"])
        redis_cap = RedisCap(cls.config, cls.instance_data, redis_http_client)
        cap = Cap(cls.config, cls.instance_data, cap_http_client)
    
    def teardown_class(cls):
        global index
        logger_info.info("teardown_class    class:%s" % cls.__name__)
        time.sleep(5)
        if index["create"] == 0:
            delete_redis_instance_step(redis_cap, resource_id)
            index["delete"] = 0
        """try:
            time.sleep(5)  # 创建失败情况等待中间层回滚
            if index["create"] == 0:
                delete_redis_instance_step(redis_cap, resource_id)
                # 如果删除执行成功，teardown时index还会加1
                # if index["reduce"] == 0:
                index["delete"] = 0
        except Exception as e:
            # 删除前请求失败的情况
            index["delete"] = 1
        """
        for i in index.items():
            print i[0] + ':' + str(i[1])
        # 输出总的监控项，正确为"0"，错误为"error_step"
        if index.values() == [0,0,0,0,0,0,0]:
            print "stab.redis.status:\"0\""
        else:
            print "stab.redis.status: error"
    
    @pytest.mark.run(order=1)
    def test_create_redis_instance(self,config, instance_data):
        global redis_cap, cap, resource_id, index
        success, redis_cap, cap, resource_id = create_an_instance_with_NP(config,instance_data,redis_http_client,cap_http_client)
        assert success == 1, "[ERROR] Create a redis instance failed"
        index['create'] = 0
    
    @pytest.mark.run(order=2)
    def test_query_cache_cluster_detail(self):
        global cluster_info, redis_cap, resource_id, index
        cluster_info = query_cache_cluster_detail(redis_cap, resource_id)
        assert cluster_info["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        index['get_detail'] = 0
    
    @pytest.mark.run(order=3)
    def test_query_filter_cache_cluster(self):
        global resource_id, cluster_info, redis_cap, index
        clusters = query_filter_cache_clusters(redis_cap)
        assert clusters != None or clusters != '', "[ERROR] Failed to get the list or redis instance"
        # 验证列表页信息与详情页一致
        verify_redis(clusters, cluster_info, resource_id)
        index['get_list'] = 0
    
    @pytest.mark.run(order=4)
    def test_update_redis(self, instance_data):
        global resource_id, cluster_info, redis_cap,cluster_info, index
        cluster_info = update_redis(instance_data, redis_cap, resource_id, cluster_info)
        # 查询详情接口验证更新信息的正确性
        space_name_update = instance_data["create_cache_cluster"]["spaceName"] + "_name_update"
        remarks_update = "remarks_update"
        billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster_info["name"] == space_name_update and cluster_info["remarks"] == remarks_update, "[ERROR] Failed to update!"
        index['update'] = 0
    
    @pytest.mark.run(order=5)
    def test_resize(self, instance_data):
        global resource_id, redis_cap, cap, index
        request_id_resize = resize_redis(redis_cap, resource_id)
        # 验证
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Failed to resize!"
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"
        index['resize'] = 0
    
    @pytest.mark.run(order=6)
    def test_reduce(self, instance_data):
        global resource_id, redis_cap, cap, index
        request_id_resize = reduce_redis(redis_cap, resource_id)
        #验证
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Failed to reduce!"
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(instance_data["create_cache_cluster"]["reduce_capacity"]), "[ERROR] The info of redis reduced is wrong!"
        index['reduce'] = 0
