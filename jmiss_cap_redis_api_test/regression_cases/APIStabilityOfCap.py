# -*- coding: utf-8 -*-

from steps.RedisOperationSteps import *
import json
import logging
import datetime

info_logger = logging.getLogger(__name__)


def print_log(log):
    print "[{0}] {1}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), log)


class APIStabilityCase:
    def __init__(self, config, instance_data):
        self.config = config
        self.instance_data = instance_data
        self.result = ["create.reason", "get_detail.reason", "get_list.reason", "update.reason",
                       "resize.reason", "reduce.reason", "delete.reason"]
        self.result_error = ["create_error", "get_detail_error", "get_list_error", "update_error",
                             "resize_error", "reduce_error", "delete_error"]
        self.index = 0
        self.space_id = ""
        self.redis_cap = None

    def __del__(self):
        # print "[TEARDOWN] Delete the redis instance %s", self.resource_id
        if self.index == 6:
            try:
                print_log("[STEP] Start to delete redis cluster {0}".format(self.space_id))
                delete_step(self.redis_cap, self.space_id)
                self.index += 1
                print_log("Delete redis cluster successfully!")
            except Exception as ee:
                abc = "Exception", ":", ee
                abc += 1
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
        redis_cap = RedisCap(self.config, self.instance_data)
        self.redis_cap = redis_cap
        # 清除残留redis实例
        print_log("[STEP] Clean up the rest redis clusters!")
        filter_data = {"filters": [{"name": "cacheInstanceName", "values": [self.instance_data["cache_instance_name"]]},
                                   {"name": "cacheInstanceStatus", "values": ["running", "error"]}]}
        clusters = query_list_step(redis_cap, filter_data)
        return
        if clusters["totalCount"] > 0:
            for cluster in clusters["cacheInstances"]:
                print_log("Delete the redis cluster [{0}]".format(cluster["cacheInstanceId"]))
                delete_step(redis_cap, cluster["cacheInstanceId"])
                time.sleep(2)
        # 创建redis实例
        print_log("[STEP] Start to create redis cluster!")
        space_id = create_step(redis_cap)
        self.space_id = space_id
        self.index += 1
        print_log("Create redis cluster successfully! The space_id is {0}".format(space_id))

        # 查询详情接口
        print_log("[STEP] Query redis cluster detail, check the status of redis instance")
        detail = query_detail_step(redis_cap, space_id)
        cluster_info = detail["cacheInstance"]
        assert cluster_info["cacheInstanceStatus"] == "running", print_log("The cluster status is not running!")
        self.index += 1
        print_log("Query redis cluster detail successfully!")

        # 查询资源列表
        print_log("[STEP] Query redis cluster list, check the meta of redis cluster")
        clusters = query_list_step(redis_cap)
        is_exist = False
        for cluster in clusters["cacheInstances"]:
            if cluster["cacheInstanceId"] == space_id:
                # 验证列表页信息与详情页一致
                assert cluster["cacheInstanceStatus"] == cluster_info["cacheInstanceStatus"] \
                       and cluster["cacheInstanceName"] == cluster_info["cacheInstanceName"] \
                       and cluster["cacheInstanceMemoryMB"] == cluster_info["cacheInstanceMemoryMB"] \
                       and cluster["connectionDomain"] == cluster_info["connectionDomain"], info_logger.error("Info of cluster list is incorrect")
                is_exist = True
        assert is_exist is True, print_log("The cluster {0} is not in cluster list".format(space_id))
        self.index += 1
        print_log("Query redis cluster list successfully!")

        # 更新实例信息
        print_log("[STEP] Start to update meta of redis cluster")
        space_name_update = self.instance_data["cache_instance_name"] + "_name_update"
        remarks_update = "remarks_update"
        update_meta_step(redis_cap, space_id, space_name_update, remarks_update)
        # 查询详情接口验证更新信息的正确性
        detail = query_detail_step(redis_cap, space_id)
        cluster_info = detail["cacheInstance"]
        assert cluster_info["cacheInstanceName"] == space_name_update and cluster_info["cacheInstanceDescription"] == remarks_update
        self.index += 1
        print_log("Update meta of redis cluster successfully!")

        # 扩容
        time.sleep(60)  # 等待一分钟，避免计费超时
        print_log("[STEP] Start to resize redis cluster")
        resize_step(redis_cap, space_id, self.instance_data["cache_resize_class"])
        detail = query_detail_step(redis_cap, space_id)
        cluster_info = detail["cacheInstance"]
        assert cluster_info["cacheInstanceStatus"] == "running" and \
               cluster_info["cacheInstanceClass"] == self.instance_data["cache_resize_class"], info_logger.error(
                "The flavor of redis resized is wrong!")
        self.index += 1
        print_log("Resize redis cluster successfully!")

        # 缩容
        time.sleep(60)  # 等待一分钟，避免计费超时
        print_log("[STEP] Start to reduce redis cluster")
        resize_step(redis_cap, space_id, self.instance_data["cache_reduce_class"])
        # 查询资源详情，验证扩容信息正确
        detail = query_detail_step(redis_cap, space_id)
        cluster_info = detail["cacheInstance"]
        assert cluster_info["cacheInstanceStatus"] == "running" and \
               cluster_info["cacheInstanceClass"] == self.instance_data["cache_reduce_class"], info_logger.error(
                "The flavor of redis reduced is wrong!")
        self.index += 1
        print_log("Reduce redis cluster successfully!")


def main():
    # region = sys.argv[1]
    conf_file = './config/config_hawkeye.json'
    instance_file = './data/data_hawkeye_hb.json'
    fd = open(conf_file, 'r')
    config = json.load(fd)
    fd.close()
    fd = open(instance_file, 'r')
    instance_data = json.load(fd)
    fd.close()
    smoke = APIStabilityCase(config, instance_data)
    smoke.run_smoke()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        abc = "Exception", ":", e
