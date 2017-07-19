# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestFailoverOfMongoInstance:
    # 创建mongo实例，验证stop mongo三个containers触发failover，failover执行完成后，mongo的状态为可用状态，副本集关系为primary, sencondary和hidden
    def _failover_mongo_containers(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Failover the primary container, the secondary container and the hidden container for the mongo instance")
	# 通过space_id查看数据库instance表获取hidden的container id
	# 调用nova api执行stop操作
	# 通过space_id查看数据库scaler_task中task_type=3的记录，获取return_code
	# 获取mongo的副本集关系
        # 验证return_code=0成功
        # 验证拓扑信息中的hidden信息不为空

    def _failover_mongo_container_for_deleted_container(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Create new container for deleted container of the mongo instance")
	# 创建mongo实例
	# 获取拓扑结构
	# 删除container，触发failover
	# 验证failover成功
	# 验证资源状态为100资源可用
