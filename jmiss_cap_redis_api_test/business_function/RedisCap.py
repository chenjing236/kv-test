# -*- coding: utf-8 -*-
import logging
from jdcloud_sdk.core.logger import *
# import json
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.services.redis.client.RedisClient import RedisClient
from jdcloud_sdk.services.redis.apis.CreateCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DeleteCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstancesRequest import *
from jdcloud_sdk.services.redis.apis.ResetCacheInstancePasswordRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceAttributeRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.DescribeOrderStatusRequest import *
from jdcloud_sdk.services.redis.apis.DescribeUserQuotaRequest import *

info_logger = logging.getLogger(__name__)


# 缓存云Redis中间层类
class RedisCap(object):
    def __init__(self, config, instance_data):
        credential = Credential(config["access_key"], config["secret_key"])
        self.client = RedisClient(credential, Config(config["host"], 'http', 30), Logger(INFO))
        # self.client = RedisClient(credential, Config('192.168.182.82:9010', 'http', 30), Logger(ERROR))
        self.instance_data = instance_data
        self.config = config
        self.region_id = instance_data["region_id"]

    # 调用sdk执行请求
    def send_request(self, request):
        response = self.client.send(request)
        assert response.error is None, info_logger.error("http request error!")
        return response

    # 创建单实例缓存云实例
    # month参数为True时，为创建包年包月资源，默认为False，按配置计费资源
    # 返回request_id和space_id
    def create(self, month=False):
        params = CreateCacheInstanceParameters(self.region_id, {
                    "cacheInstanceName": self.instance_data["cache_instance_name"],
                    "cacheInstanceDescription": self.instance_data["cache_instance_description"],
                    "password": self.instance_data["password"],
                    "cacheInstanceClass": self.instance_data["cache_instance_class"],
                    "vpcId": self.instance_data["vpc_id"],
                    "subnetId": self.instance_data["subnet_id"],
                    "azId": {
                        "master": self.instance_data["master_az_id"],
                        "slave": self.instance_data["slaver_az_id"]}})
        if month is True:
            params.setCharge({
                "chargeDuration": self.instance_data["charge_duration"],
                "chargeMode": self.instance_data["charge_mode"],
                "chargeUnit": self.instance_data["charge_unit"]})
        request = CreateCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result["cacheInstanceId"]

    # 查询云缓存实例详情
    # 参数为space_id
    # 返回request_id和详情结果
    def query_detail(self, space_id):
        params = DescribeCacheInstanceParameters(self.region_id, space_id)
        request = DescribeCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result

    # 根据过滤条件查云缓存实例列表
    # 参数为过滤条件，例如：
    # {
    #   "filters":[{"name":"instanceType","values":["changing"]}],
    #   "pageNumber":1,
    #   "pageSize":10,
    #   "sorts":[{"direction":"desc","name":"createTime"}]
    # }
    # 返回request_id和列表结果
    def query_list(self, filter_data=None):
        params = DescribeCacheInstancesParameters(self.region_id)
        # print filter_data
        # print filter_data["filters"]
        # print json.dumps(filter_data["filters"])
        if "filters" in filter_data:
            params.setFilters(filter_data["filters"])
        # if "pageNumber" in filter_data:
        #     params.setPageNumber(4)
        # if "pageSize" in filter_data:
        #     params.setPageSize(5)
        # if "sorts" in filter_data:
        #     params.setSorts(filter_data["sorts"])
        request = DescribeCacheInstancesRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result

    # 查询订单状态，如创建、扩容等操作的当前状态
    # 参数为查询操作的request_id
    # 返回request_id，操作状态：success、fail、in_process
    def query_order_status(self, request_id):
        params = DescribeOrderStatusParameters(self.region_id, request_id)
        request = DescribeOrderStatusRequest(params)
        response = self.send_request(request)
        if response.result["success"] == 1:
            return response.request_id, 'success'
        elif response.result["inProcess"] == 1:
            return response.request_id, 'in_process'
        else:
            return response.request_id, 'fail'

    # 更新缓存云实例基本信息
    # 参数为space_id，要修改的name和description，name不能为空
    # 返回request_id
    def update_meta(self, space_id, name=None, description=None):
        params = ModifyCacheInstanceAttributeParameters(self.region_id, space_id)
        params.setCacheInstanceName(name)
        params.setCacheInstanceDescription(description)
        request = ModifyCacheInstanceAttributeRequest(params)
        response = self.send_request(request)
        return response.request_id

    # 重置云缓存密码
    # 参数为space_id，要修改的password，传空字符串为免密
    # 返回request_id
    def reset_password(self, space_id, password):
        params = ResetCacheInstancePasswordParameters(self.region_id, space_id)
        params.setPassword(password)
        request = ResetCacheInstancePasswordRequest(params)
        response = self.send_request(request)
        return response.request_id

    # 删除云缓存实例
    # 参数为space_id
    # 返回request_id
    def delete(self, space_id):
        params = DeleteCacheInstanceParameters(self.region_id, space_id)
        request = DeleteCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id

    # redis扩容缩容
    # 参数为space_id，资源规格代码instance_class
    # 返回request_id
    def resize(self, space_id, instance_class):
        params = ModifyCacheInstanceClassParameters(self.region_id, space_id, instance_class)
        request = ModifyCacheInstanceClassRequest(params)
        response = self.send_request(request)
        return response.request_id

    # 查询redis实例规格列表
    # 参数为region_id
    # 返回request_id和实例规格列表
    def query_flavor(self):
        params = DescribeInstanceClassParameters(self.region_id)
        request = DescribeInstanceClassRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result

    # 查询用户当前已使用配额
    # 参数为region_id
    # 返回request_id，总配额max和当前已使用配额used
    def query_quota(self):
        params = DescribeUserQuotaParameters(self.region_id)
        request = DescribeUserQuotaRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result["quota"]["max"], response.result["quota"]["used"]
