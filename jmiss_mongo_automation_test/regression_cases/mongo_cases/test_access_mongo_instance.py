# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestAccessMongoInstance:
    # 创建mongo实例，验证通过绑定外网IP的VM访问mongo实例，可以执行读写操作
    @pytest.mark.smoke
    def _access_mongo_instance(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Access a mongo instance with a VM that binds a internet IP")
	# 获取mongo实例的domain信息
        # 通过VM访问mongo实例
        # 对mongo实例执行写操作
        # 获取写入mongo实例的数据

    #mongo实例执行failover成功后，访问mongo实例
    @pytest.mark.smoke
    def _access_mongo_instance_after_failover(self, create_mongo_instance):
	info_logger.info("[SCENARIOT] Access the mongo instance after doing failover successfully")
	#创建mongo实例
	#执行failover，stop primary container触发failovr
	#验证failover成功
	#访问mongo实例，进行读写操作
