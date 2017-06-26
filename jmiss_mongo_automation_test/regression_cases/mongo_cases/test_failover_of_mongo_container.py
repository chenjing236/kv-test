# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestFailoverOfMongoInstance:
    # 创建mongo实例，验证stop mongo三个containers触发failover，failover执行完成后，mongo的状态为可用状态，副本集关系为primary, sencondary和hidden
    def _failover_mongo_containers(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Failover the primary container, the secondary container and the hidden container for the mongo instance")
	# 获取mongo的副本集关系
	# 同时stop mongo实例的三个containers,触发failover
	# 获取failover的操作结果，即查看failover是否完成，及完成的状态
	# 获取mongo的副本集关系

    def _failover_mongo_container_for_deleted_container(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Create new container for deleted container of the mongo instance")
	# 创建mongo实例
	# 获取拓扑结构
	# 删除container，触发failover
	# 验证failover成功
	# 验证资源状态为100资源可用
