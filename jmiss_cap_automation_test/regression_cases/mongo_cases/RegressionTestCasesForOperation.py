# -*- coding: utf-8 -*-
import pytest
import logging
from BasicTestCase import *
info_logger = logging.getLogger(__name__)

# 运营接口的测试用例
class TestSmokeCasesForOperation:
    # 运营系统，删除资源
    @pytest.mark.smoke
    def test_delete_resource(self, config, instance_data, cap_http_client, mongo_http_client, create_mongo_instance_with_yearly_fee):
	info_logger.info("[Scenario] Delete mongo instance using operation delete action")
	# 创建mongo实例,类型为包年包月的资源
	resource_id, mongo_info = create_mongo_instance_with_yearly_fee

