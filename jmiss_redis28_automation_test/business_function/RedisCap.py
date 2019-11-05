# -*- coding: utf-8 -*-
import logging
# import string
# import random
import base64
# import requests
from jdcloud_sdk.core.logger import *
# import json
import datetime
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import *
from jdcloud_sdk.services.redis.client.RedisClient import RedisClient
from jdcloud_sdk.services.redis.apis.CreateBackupRequest import *
# from jdcloud_sdk.services.redis.apis.CreateCacheInstanceNoBillRequest import *
from jdcloud_sdk.services.redis.apis.CreateCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DeleteCacheInstanceRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeAdminConfigRequest import *
from jdcloud_sdk.services.redis.apis.DescribeBackupPolicyRequest import *
from jdcloud_sdk.services.redis.apis.DescribeBackupsRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.DescribeCacheInstancesRequest import *
from jdcloud_sdk.services.redis.apis.DescribeClusterInfoRequest import *
from jdcloud_sdk.services.redis.apis.DescribeDownloadUrlRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.DescribeInstanceConfigRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeInstanceNamesRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeIpWhiteListRequest import *
from jdcloud_sdk.services.redis.apis.DescribeOrderStatusRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeProxyConfigRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeRedisConfigRequest import *
from jdcloud_sdk.services.redis.apis.DescribeSlowLogRequest import *
# from jdcloud_sdk.services.redis.apis.DescribeSupportedFunctionRequest import *
from jdcloud_sdk.services.redis.apis.DescribeUserQuotaRequest import *
from jdcloud_sdk.services.redis.apis.ModifyBackupPolicyRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceAttributeRequest import *
from jdcloud_sdk.services.redis.apis.ModifyCacheInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceClassRequest import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceConfigRequest import *
# from jdcloud_sdk.services.redis.apis.ModifyIpWhiteListRequest import *
from jdcloud_sdk.services.redis.apis.ModifyUserQuotaRequest import *
from jdcloud_sdk.services.redis.apis.ResetCacheInstancePasswordRequest import *
from jdcloud_sdk.services.redis.apis.RestoreInstanceRequest import *
# from jdcloud_sdk.services.redis.apis.StartInstanceRequest import *
# from jdcloud_sdk.services.redis.apis.StopInstanceRequest import *

info_logger = logging.getLogger(__name__)


# 缓存云Redis中间层类
class RedisCap:
    def __init__(self, config, instance_data, log_level=Logger(FATAL)):
        credential = Credential(config["access_key"], config["secret_key"])
        self.client = RedisClient(credential, Config(str(config["cap_host"]), SCHEME_HTTP, 60), log_level)
        self.instance_data = instance_data
        self.config = config
        self.region_id = instance_data["region_id"]
        self.header = {'x-jdcloud-erp': base64.b64encode(config["erp"])}

    # 调用sdk执行请求
    def send_request(self, request):
        start_time = datetime.datetime.now()
        # print "[TIME] Request start time is {0}".format(start_time)
        response = self.client.send(request)
        end_time = datetime.datetime.now()
        exec_time = (end_time - start_time).microseconds/1000
        if exec_time > 500:
            print "[TIME] Request exec time is {0} milliseconds".format(exec_time)
        assert 'response' in locals().keys()
        # if response.error is not None:
        #     print "[hello]", response.error.code, response.error.message, response.error.status
        # print "[hello]", response.result
        # assert response.error is None, info_logger.error("http request error!")
        return response

    # 创建备份
    # 参数为space_id，要修改的name和description，name不能为空
    # 返回request_id
    def create_backup(self, space_id, file_name, backup_type=1):
        params = CreateBackupParameters(self.region_id, space_id, file_name, backup_type)
        request = CreateBackupRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 创建单实例缓存云实例
    # month参数为True时，为创建包年包月资源，默认为False，按配置计费资源
    # 返回request_id和space_id
    def create(self, create_params, charge_params=None):
        params = CreateCacheInstanceParameters(self.region_id, create_params)
        if charge_params is not None:
            params.setCharge(charge_params)
        request = CreateCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 删除云缓存实例
    # 参数为space_id, op_delete为1时，代表运营删除，为0时，代表普通删除
    # 返回request_id
    def delete(self, space_id, op_delete=0):
        params = DeleteCacheInstanceParameters(self.region_id, space_id)
        if op_delete == 1:  # 运营删除
            request = DeleteCacheInstanceRequest(params, self.header)
        else:   # 普通删除
            request = DeleteCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # 查询云缓存实例备份策略
    # 参数为space_id
    # 返回request_id和详情结果
    def query_backup_policy(self, space_id):
        params = DescribeBackupPolicyParameters(self.region_id, space_id)
        request = DescribeBackupPolicyRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 查询云缓存实例备份列表
    # 参数为space_id
    # 参数为filter_data，例如：
    # {
    #   "pageNumber": 1,
    #   "pageSize": 10,
    #   "startTime": "",
    #   "endTime": "",
    #   "baseId": ""
    # }
    # 返回request_id和备份列表
    def query_backup_list(self, space_id, filter_data=None):
        if filter_data is None:
            filter_data = {}
        params = DescribeBackupsParameters(self.region_id, space_id)
        if "pageNumber" in filter_data:
            params.setPageNumber(filter_data["pageNumber"])
        if "pageSize" in filter_data:
            params.setPageSize(filter_data["pageSize"])
        if "startTime" in filter_data:
            params.setStartTime(filter_data["startTime"])
        if "endTime" in filter_data:
            params.setEndTime(filter_data["endTime"])
        if "baseId" in filter_data:
            params.setBaseId(filter_data["baseId"])
        request = DescribeBackupsRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 查询云缓存实例详情
    # 参数为space_id
    # 返回request_id和详情结果
    def query_detail(self, space_id):
        params = DescribeCacheInstanceParameters(self.region_id, space_id)
        request = DescribeCacheInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 根据过滤条件查云缓存实例列表
    # 参数为过滤条件，例如：
    # {
    #   "filters":[{"name":"instanceType","values":["changing"]}],
    #   "pageNumber":1,
    #   "pageSize":10,
    #   "sorts":[{"direction":"desc","name":"createTime"}],
    #   "tagFilters":[{"key":["value1","value2"]}]
    # }
    # 返回request_id和列表结果
    def query_list(self, filter_data=None):
        if filter_data is None:
            filter_data = {}
        params = DescribeCacheInstancesParameters(self.region_id)
        if "filters" in filter_data:
            params.setFilters(filter_data["filters"])
        if "pageNumber" in filter_data:
            params.setPageNumber(filter_data["pageNumber"])
        if "pageSize" in filter_data:
            params.setPageSize(filter_data["pageSize"])
        if "sorts" in filter_data:
            params.setSorts(filter_data["sorts"])
        if "tagFilters" in filter_data:
            params.setTagFilters(filter_data["tagFilters"])
        # print params.filters
        request = DescribeCacheInstancesRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 查询集群的内部拓扑信息
    # 参数为space_id
    # 返回request_id和详情结果
    def query_cluster_info(self, space_id):
        params = DescribeClusterInfoParameters(self.region_id, space_id)
        request = DescribeClusterInfoRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 获取实例备份文件临时下载地址
    # 参数为space_id，base_id
    # 返回request_id和详情结果
    def query_download_url(self, space_id, base_id):
        # base_id必须为str类型，从接口中读出的参数均为unicode类型，需要转换下
        params = DescribeDownloadUrlParameters(self.region_id, space_id, str(base_id))
        request = DescribeDownloadUrlRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 查询redis实例规格列表
    # 参数为region_id
    # 返回request_id和实例规格列表
    def query_flavor(self):
        params = DescribeInstanceClassParameters(self.region_id)
        request = DescribeInstanceClassRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 查询redis实例当前的配置参数
    # 参数为region_id，space_id
    # 返回request_id和实例当前配置参数
    def query_config(self, space_id):
        params = DescribeInstanceConfigParameters(self.region_id, space_id)
        request = DescribeInstanceConfigRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

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

    # 根据过滤条件查询实例慢查询日志
    # 参数为过滤条件，例如：
    # {
    #   "pageNumber": 1,
    #   "pageSize": 10,
    #   "startTime": "",
    #   "endTime": "",
    #   "shardId": 1
    # }
    # 返回request_id和列表结果
    def query_slow_log(self, space_id, filter_data=None):
        if filter_data is None:
            filter_data = {}
        params = DescribeSlowLogParameters(self.region_id, space_id)
        if "pageNumber" in filter_data:
            params.setPageNumber(filter_data["pageNumber"])
        if "pageSize" in filter_data:
            params.setPageSize(filter_data["pageSize"])
        if "startTime" in filter_data:
            params.setStartTime(filter_data["startTime"])
        if "endTime" in filter_data:
            params.setEndTime(filter_data["endTime"])
        if "shardId" in filter_data:
            params.setShardId(filter_data["shardId"])
        request = DescribeCacheInstancesRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result

    # 查询用户当前已使用配额
    # 参数为region_id
    # 返回request_id，总配额max和当前已使用配额used
    def query_quota(self):
        params = DescribeUserQuotaParameters(self.region_id)
        request = DescribeUserQuotaRequest(params)
        response = self.send_request(request)
        return response.request_id, response.result, response.error

    # 修改资源备份策略
    # 参数为space_id，要修改的backup_time, backup_period
    # 返回request_id
    def modify_backup_policy(self, space_id, backup_time, backup_period):
        params = ModifyBackupPolicyParameters(self.region_id, space_id, backup_time, backup_period)
        request = ModifyBackupPolicyRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # 更新缓存云实例基本信息
    # 参数为space_id，要修改的name和description，name不能为空
    # 返回request_id
    def update_meta(self, space_id, name=None, description=None):
        params = ModifyCacheInstanceAttributeParameters(self.region_id, space_id)
        params.setCacheInstanceName(name)
        params.setCacheInstanceDescription(description)
        request = ModifyCacheInstanceAttributeRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # redis扩容缩容
    # 参数为space_id，资源规格代码instance_class
    # 返回request_id
    def resize(self, space_id, instance_class):
        params = ModifyCacheInstanceClassParameters(self.region_id, space_id, instance_class)
        request = ModifyCacheInstanceClassRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # 运营修改用户可见flavor
    # 参数为规格代码instance_class，操作类型action_type：1可见，0无效，-1不可见
    # 返回request_id
    def modify_user_class(self, instance_class, action_type):
        params = ModifyInstanceClassParameters(self.region_id, instance_class, action_type)
        request = ModifyInstanceClassRequest(params, self.header)
        response = self.send_request(request)
        return response.request_id, response.error

    # 修改实例自定义参数
    # 参数为space_id，实例的规格列表instance_config
    # 返回request_id
    def modify_config(self, space_id, redis_config):
        params = ModifyInstanceConfigParameters(self.region_id, space_id, redis_config)
        request = ModifyInstanceConfigRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # 运营修改用户资源配额
    # 参数为已使用配额used，配额总数quota
    # 返回request_id
    def modify_quota(self, used, quota):
        params = ModifyUserQuotaParameters(self.region_id, used, quota)
        request = ModifyUserQuotaRequest(params, self.header)
        response = self.send_request(request)
        return response.request_id, response.error

    # 重置云缓存密码
    # 参数为space_id，要修改的password，传空字符串为免密
    # 返回request_id
    def reset_password(self, space_id, password):
        params = ResetCacheInstancePasswordParameters(self.region_id, space_id)
        params.setPassword(password)
        request = ResetCacheInstancePasswordRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error

    # 使用备份文件恢复实例数据
    # 参数为space_id，base_id
    # 返回request_id
    def restore(self, space_id, base_id):
        params = RestoreInstanceParameters(self.region_id, space_id, base_id)
        request = RestoreInstanceRequest(params)
        response = self.send_request(request)
        return response.request_id, response.error
