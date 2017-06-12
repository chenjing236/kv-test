#!/usr/bin/python
# -*- coding: utf-8 -*- 

import httplib
import json

#缓存云-CAP,REDIS&MONGO的HTTP Client
class RedisCapClient(object):
    def __init__(self, host, service):
        self.host = host
	self.service = service

    # http请求
    def http_request(self, method, uri, data=None):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}".format(uri), data)
	res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    # 将json对象装换为string类型
    def to_json_string(self, args):
        return json.dumps(args)

    # 创建云缓存实例
    def create_cache_cluster(self, args):
	return self.http_request("POST", "cache?action=createCacheCluster", args)

    # 更新云缓存基本信息
    def update_cache_cluster(self, args):
	return self.http_request("POST", "cache?action=updateCacheCluster", args)

    # 变配缓存实例，即扩容&缩容
    def modify_cache_cluster(self, args):
	return self.http_request("POST", "cache?action=modifyCacheCluster", args)

    # 获取实时被使用内存信息
    def real_time_info_cache_cluster(self, args, space_ids):
	uri = "cache?action=realTimeInfoCacheCluster" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&spaceIds=" + space_id
	return self.http_request("GET", uri)

    # 查询云缓存实例列表
    def query_cache_clusters(self, args):
        uri = "cache?action=queryCacheClusters" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"]
        return self.http_request("GET", uri)

    # 使用过滤条件查询云缓存实例列表
    def query_filter_cache_clusters(self, args):
        uri = "cache?action=queryFilterCacheClusters" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&filterName=" + args["filter_name"] + "&filterSpaceType=" + args["filter_space_type"] + "&filterStatus=" + args["filter_status"] + "&sortName=" + args["sort_name"] + "&sortRule=" + args["sort_rule"] + "&pageSize=" + args["page_size"] + "&pageNum=" + args["page_num"] + "&category=" + args["category"]
        return self.http_request("GET", uri)

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, args, cluster_id):
        uri = "cache?action=queryCacheClusterDetail" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&clusterId=" + cluster_id
        return self.http_request("GET", uri)

    # 删除云缓存实例
    def delete_cache_cluster(self, args, cluster_id):
        uri = "cache?action=deleteCacheCluster" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&clusterId=" + cluster_id
        return self.http_request("DELETE", uri)

    # 批量删除云缓存实例
    def delete_cache_clusters(self, args, cluster_ids):
        uri = "cache?action=deleteCacheClusters" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&clusterIds=" + cluster_ids
        return self.http_request("DELETE", uri)

    # 查询云缓存监控信息
    def query_cache_monitor_metric(self, args, cluster_id, period, period_time_unit):
        uri = "cache?action=queryCacheMonitorMetric" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&clusterId=" + cluster_id + "&period=" + period + "&periodTimeUnit=" + period_time_unit
        return self.http_request("GET", uri)

    # 根据订单查询缓存云实例详情
    def query_cache_cluster_detail_by_order(self, args, order_id, cluster_id):
        uri = "cache?action=queryCacheClusterDetailByOrder" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&orderId=" + order_id + "&clusterId=" + cluster_id
        return self.http_request("GET", uri)

    # 启动缓存云实例
    def start_cache_cluster(self, space_id):
        uri = "cache?action=startCacheCluster" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&spaceId=" + space_id
        return self.http_request("GET", uri)

    # 停服缓存云实例
    def stop_cache_cluster(self, space_id):
        uri = "cache?action=stopCacheCluster" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&spaceId=" + space_id
        return self.http_request("GET", uri)

    # 获取规格
    def query_flavors(self, type):
        uri = "cache?action=queryFlavors" + "&account=" + args["account"] + "&dataCenter=" + args["data_center"] + "&user=" + args["user"] + "&type=" + type
        return self.http_request("GET", uri)


#缓存云-CAP HTTP Client
class CapClient(object):
    # 用户中心 - 获得用户配额
    def query_user_quota(self, resource):
        return self.http_request("GET", "user?action=queryUserQuota&resource={0}".format(resource))

    # 用户中心 - 修改已用配额接口
    def modify_quota(self, args):
	return self.http_request("POST", "user?action=modifyQuota", data)

    # 订单支付
    def pay(self, args):
	return self.http_request("POST", "billing?action=pay", args)

