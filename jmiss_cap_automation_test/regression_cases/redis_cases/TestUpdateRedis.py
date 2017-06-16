# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestUpdateRedis:

    @pytest.mark.smoke
    def test_update_meta(self, create_redis_instance):
        return
        # 创建云缓存实例，支付成功，验证资源状态为100
        # 调用查询详情接口，获取资源name和remarks等信息
        # 调用更新基本信息接口更新资源name和remarks，验证接口调用成功
        # 调用查询详情接口，获取资源修改后的name和remarks信息
        # 验证修改后的name和remarks正确

    @pytest.mark.smoke
    def test_reset_password(self, create_redis_instance):
        return
        # 创建云缓存实例，支付成功，验证资源状态为100
        


