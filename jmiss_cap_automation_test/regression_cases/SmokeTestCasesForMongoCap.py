# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoCap:
    @pytest.mark.smoke
    def test_create_an_instance(self, config, create_mongo_instance):
        info_logger.info("[Scenario] Create an instance for mongo, the instance consists of a primary container, a secondary container and a hidden container")
        cluster_id = create_mongo_instance
        info_logger.info("[INFO] The cluster id is %s for creating a mongo instance", cluster_id)
