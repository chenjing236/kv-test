# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestGetMongoDetailInfo:
    #获取mongo实例的详细信息
    def _get_mongo_detail_info(self, config, instance_data, http_client):
	info_logger.info("[SCENARIO] Get the detail info for the mongo instance")
