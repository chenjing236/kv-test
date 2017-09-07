# -*- coding: utf-8 -*-

from BasicTestCase import *
from utils.HttpClient import RedisCapClient, CapClient
import time

logger_info = logging.getLogger(__name__)


class APIStabilityCase:
    def __init__(self, config, instance_data, redis_http_client, cap_http_client):
        self.config = config
        self.instance_data = instance_data
        self.redis_http_client = redis_http_client
        self.cap_http_client = cap_http_client
        self.result = ["create.reason", "get_detail.reason", "get_list.reason", "update.reason",
                       "resize.reason", "reduce.reason", "delete.reason"]
        self.result_error = ["create_error", "get_detail_error", "get_list_error", "update_error",
                             "resize_error", "reduce_error", "delete_error"]
        self.index = 0
        self.resource_id = ""
    '''
    def __del__(self):
        # print "[TEARDOWN] Delete the redis instance %s", self.resource_id
        try:
            time.sleep(5)  # 创建失败情况等待中间层回滚
            delete_redis_instance_step(self.redis_cap, self.resource_id)
            # 如果删除前执行失败了，teardown时index还会加1，不准确
            if self.index == 6:
                self.index += 1
        except Exception as e:
            # 删除请求失败的情况
            self.index = 6
        # self.index += 1
        i = 0
        while i < len(self.result):
            if i == self.index:
                print self.result[i] + ":1"
            else:
                print self.result[i] + ":0"
            i += 1
        # 输出总的监控项，正确为"0"，错误为"error_step"
        if self.index == 7:
            print "stab.redis.status:\"0\""
        else:
            print "stab.redis.status:\"{0}\"".format(self.result_error[self.index])
    '''

    def __del__(self):
        # print "[TEARDOWN] Delete the redis instance %s", self.resource_id
        try:
            time.sleep(5)  # 创建失败情况等待中间层回滚
            if self.index != 0:
                delete_redis_instance_step(self.redis_cap, self.resource_id)
                # 如果删除执行成功，teardown时index还会加1，不准确
                if self.index == 6:
                    self.index += 1
        except Exception as e:
            # 删除前请求失败的情况
            self.index = 6
        # self.index += 1
        i = 0
        while i < len(self.result):
            if i == self.index:
                print self.result[i] + ":1"
            else:
                print self.result[i] + ":0"
            i += 1
        # 输出总的监控项，正确为"0"，错误为"error_step"
        if self.index == 7:
            print "stab.redis.status:\"0\""
        else:
            print "stab.redis.status:\"{0}\"".format(self.result_error[self.index])

    def run_smoke(self):
        # print "[Scenario] Create an instance for redis, the instance consists of a master and a slave"
        redis_cap = RedisCap(self.config, self.instance_data, self.redis_http_client)
        self.redis_cap = redis_cap
        cap = Cap(self.config, self.instance_data, self.cap_http_client)
        # 清除残留redis实例
        clusters = query_filter_cache_clusters_step(redis_cap, {"filterName": self.instance_data["create_cache_cluster"]["spaceName"], "filterSpaceType": 1, "category": "1"})
        # print clusters
        if clusters is not None:
            for cluster in clusters:
                delete_redis_instance_step(self.redis_cap, cluster["spaceId"])
                time.sleep(2)
        # 创建redis实例
        # print "[STEP] Create an instance for redis, the instance consists of a master and a slave"
        request_id_for_redis = create_redis_instance_step(redis_cap)
        # print request_id_for_redis
        # 支付
        # print "[STEP] Pay for the create order of redis instance"
        # pay_for_redis_instance_step(cap, request_id_for_redis, self.instance_data["redis_coupon_info"]["discountId"], self.instance_data["redis_coupon_info"]["discountValue"])
        # 查询订单状态
        # print "[STEP] Query order status, check the status of order"
        success, resource_id = query_order_status_step(cap, request_id_for_redis)
        self.resource_id = resource_id
        self.index += 1

        # 查询详情接口
        # print "[STEP] Query redis instance detail, check the status of redis instance"
        billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster_info["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        # print "success"
        self.index += 1


        # 查询详情列表
        # print "[STEP] Query redis instance detail list"
        clusters = query_filter_cache_clusters_step(redis_cap, {})
        for cluster in clusters:
            assert cluster["status"] != 102, "[ERROR] There is a cluster which status equals 102 in the cluster list"
            if cluster["spaceId"] == resource_id:
                # 验证列表页信息与详情页一致
                assert cluster["status"] == cluster_info["status"] and cluster["name"] == cluster_info["name"] and \
                       cluster["spaceType"] == cluster_info["spaceType"] and cluster["zoneId"] == cluster_info["zoneId"] and \
                       cluster["capacity"] == cluster_info["capacity"] and cluster["domain"] == cluster_info["domain"], "[ERROR] Info of cluster list is incorrect"
                # print "[INFO] Info of cluster list is correct, status={0}, name={1}, spaceType={2}, zoneId={3}, " \
                #       "capacity={4}, domain={5}".format(cluster["status"], cluster["name"], cluster["spaceType"], cluster["zoneId"],
                #                                         cluster["capacity"], cluster["domain"])
                is_exist = True
        assert is_exist is True, "[ERROR] The cluster {0} is not in cluster list".format(resource_id)
        self.index += 1

        # 更新实例信息
        # print "[STEP] Update info"
        space_name_update = self.instance_data["create_cache_cluster"]["spaceName"] + "_name_update"
        remarks_update = "remarks_update"
        mark = "updatebaseinfo"
        update_cache_cluster_step(redis_cap, resource_id, {"spaceName": space_name_update, "remarks": remarks_update, "mark": mark})
        # 查询详情接口验证更新信息的正确性
        billing_order, cluster_info = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster_info["name"] == space_name_update and cluster_info["remarks"] == remarks_update
        self.index += 1

        # 扩容
        # print "[STEP] resize big"
        time.sleep(60)  # 等待一分钟，避免计费超时
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 1)
        #pay_for_redis_instance_step(cap, request_id_resize, self.instance_data["redis_coupon_info"]["discountId"], self.instance_data["redis_coupon_info"]["discountValue"])
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query resize order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Redis resize failed!"
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(self.instance_data["create_cache_cluster"]["resize_capacity"]), "[ERROR] The info of redis resized is wrong!"
        self.index += 1

        # 缩容
        # print "[STEP] reduce"
        time.sleep(60)  # 等待一分钟，避免计费超时
        request_id_resize = modify_cache_cluster_step(redis_cap, resource_id, 0)
        # 调用支付接口
        # info_logger.info("[STEP] Pay for reduce order")
        # pay_for_redis_instance_step(cap, request_id_resize, self.instance_data["redis_coupon_info"]["discountId"], self.instance_data["redis_coupon_info"]["discountValue"])
        # 查询订单状态，验证扩容成功
        info_logger.info("[STEP] Query reduce order status until resize over")
        success, resource_id = query_order_status_step(cap, request_id_resize)
        assert success == 1, "[ERROR] Reduce resize failed!"
        # 查询资源详情，验证扩容信息正确
        info_logger.info("[STEP] Query redis cluster detail, check the redis info")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        assert cluster["status"] == 100 and cluster["capacity"] == int(self.instance_data["create_cache_cluster"]["reduce_capacity"]), "[ERROR] The info of redis reduced is wrong!"
        self.index += 1

        '''
        # realtime info
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
        self.index += 1
        '''


def main():
    conf_file = '../../config/redis_config/config_hawkeye.json'
    instance_file = '../../data/redis_data/data_hawkeye.json'
    fd = open(conf_file, 'r')
    config = json.load(fd)
    fd.close()
    fd = open(instance_file, 'r')
    instance_data = json.load(fd)
    fd.close()
    redis_http_client = RedisCapClient(config["host"])
    cap_http_client = CapClient(config["host"])
    smoke = APIStabilityCase(config, instance_data, redis_http_client, cap_http_client)
    smoke.run_smoke()
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        abc = "Exception", ":", e
