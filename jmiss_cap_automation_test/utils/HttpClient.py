#!/usr/bin/python
# -*- coding: utf-8 -*- 

import httplib
import json


# 缓存云-CAP,REDIS&MONGO的HTTP Client
class RedisCapClient(object):
    def __init__(self, host):
        self.host = host
        # self.service = service

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
        return self.http_request("POST", "cache?action=createCacheCluster", json.dumps(args))

    # 更新云缓存基本信息
    def update_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=updateCacheCluster", json.dumps(args))

    # 变配缓存实例，即扩容&缩容
    def modify_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=modifyCacheCluster", json.dumps(args))

    # 获取实时被使用内存信息
    def real_time_info_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=realTimeInfoCacheCluster", json.dumps(args))

    # 查询云缓存实例列表
    def query_cache_clusters(self, args):
        return self.http_request("POST", "cache?action=queryCacheClusters", json.dumps(args))

    # 使用过滤条件查询云缓存实例列表
    def query_filter_cache_clusters(self, args):
        return self.http_request("POST", "cache?action=queryFilterCacheClusters", json.dumps(args))

    # 查询云缓存实例详情
    def query_cache_cluster_detail(self, args):
        return self.http_request("POST", "cache?action=queryCacheClusterDetail", json.dumps(args))

    # 删除云缓存实例
    def delete_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=deleteCacheCluster", json.dumps(args))

    # 批量删除云缓存实例
    def delete_cache_clusters(self, args):
        return self.http_request("POST", "cache?action=deleteCacheClusters", json.dumps(args))

    # 查询云缓存监控信息
    def query_cache_monitor_metric(self, args):
        return self.http_request("POST", "cache?action=queryCacheMonitorMetric", json.dumps(args))

    # 根据订单查询缓存云实例详情
    def query_cache_cluster_detail_by_order(self, args):
        return self.http_request("POST", "cache?action=queryCacheClusterDetailByOrder", json.dumps(args))

    # 启动缓存云实例
    def start_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=startCacheCluster", json.dumps(args))

    # 停服缓存云实例
    def stop_cache_cluster(self, args):
        return self.http_request("POST", "cache?action=stopCacheCluster", json.dumps(args))

    # 获取规格
    def query_flavors(self, args):
        return self.http_request("POST", "cache?action=queryFlavors", json.dumps(args))

class MongoCapClient(object):
    def __init__(self, host):
        self.host = host

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

    # 创建mongo实例
    def create_mongo_db(self, args):
	return self.http_request("POST", "mongoDb?action=createMongoDb", json.dumps(args))

    # 查询monggo详情
    def query_mongo_db_detail(self, args):
	return self.http_request("POST", "mongoDb?action=queryMongoDbDetail", json.dumps(args))

    # 删除mongo实例
    def delete_mongo_db(self, args):
	return self.http_request("POST", "mongoDb?action=deleteMongoDb", json.dumps(args))

    # 修改名字
    def modify_mongo_db_name(self, args):
	return self.http_request("POST", "mongoDb?action=modifyMongoDbName", json.dumps(args))

    # 查看flavor信息
    def query_flavors(self, args):
	return self.http_request("POST", "mongoDb?action=queryFlavors", json.dumps(args))

#缓存云-CAP HTTP Client
class CapClient(object):
    def __init__(self, host):
        self.host = host

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

    # 用户中心 - 获得用户配额
    def query_user_quota(self, args):
        return self.http_request("POST", "user?action=queryUserQuota", json.dumps(args))

    # 用户中心 - 修改已用配额接口
    def modify_quota(self, args):
        return self.http_request("POST", "user?action=modifyQuota", json.dumps(args))

    # 订单支付
    def pay(self, args):
        return self.http_request("POST", "billing?action=pay", json.dumps(args))

    def query_order_status(self, args):
        return self.http_request("POST", "order?action=queryOrderStatus", json.dumps(args))
