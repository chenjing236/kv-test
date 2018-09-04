# -*- coding: utf-8 -*-
import logging
import base64
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.services.redis.client.RedisClient import RedisClient
from jdcloud_sdk.services.redis.apis.DeleteCacheInstanceRequest import *
from jdcloud_sdk.services.redis.apis.ModifyUserQuotaRequest import *
from jdcloud_sdk.services.redis.apis.ModifyInstanceClassRequest import *

info_logger = logging.getLogger(__name__)


# 缓存云Redis中间层类
class RedisOperation(object):
    def __init__(self, config, instance_data):
        credential = Credential(config["access_key"], config["secret_key"])
        self.client = RedisClient(credential, Config(config["host_internal"], 'http'))
        self.region_id = instance_data["region_id"]
        self.header = {'x-jdcloud-erp': base64.b64encode(config["erp"])}

    # 调用sdk执行请求
    def send_request(self, request):
        response = self.client.send(request)
        assert response.error is None, info_logger.error("http request error!")
        return response

    # 运营删除云缓存实例（包年包月资源）
    # 参数为space_id
    # 返回request_id
    def delete(self, space_id):
        params = DeleteCacheInstanceParameters(self.region_id, space_id)
        request = DeleteCacheInstanceRequest(params, self.header)
        response = self.send_request(request)
        return response.request_id

    # 运营修改用户资源配额
    # 参数为已使用配额used，配额总数quota
    # 返回request_id
    def modify_quota(self, used, quota):
        params = ModifyUserQuotaParameters(self.region_id, used, quota)
        request = ModifyUserQuotaRequest(params, self.header)
        response = self.send_request(request)
        return response.request_id

    # 运营修改用户可见flavor
    # 参数为规格代码instance_class，操作类型action_type：1可见，0无效，-1不可见
    # 返回request_id
    def modify_user_class(self, instance_class, action_type):
        params = ModifyInstanceClassParameters(self.region_id, instance_class, action_type)
        request = ModifyInstanceClassRequest(params, self.header)
        response = self.send_request(request)
        return response.request_id
