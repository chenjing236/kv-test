# -*- coding: utf-8 -*- 

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForRedisCap:
    @pytest.mark.smoke
    def test_create_an_instance(self, config, create_redis_instance):
	info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
	request_id = create_redis_instance
	info_logger.info("[INFO] The request id is %s for creating a redis instance", request_id)
