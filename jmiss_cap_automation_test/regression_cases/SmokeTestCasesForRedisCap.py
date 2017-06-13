# -*- coding: utf-8 -*- 

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestSmokeCasesForRedisCap:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, create_redis_instance):
        info_logger.info("[Scenario] Create an instance for redis, the instance consists of a master and a slave")
        request_id, resource_id = create_redis_instance
        info_logger.info("[INFO] Test create redis instance successfully, the resourceId is {0}".format(resource_id))
