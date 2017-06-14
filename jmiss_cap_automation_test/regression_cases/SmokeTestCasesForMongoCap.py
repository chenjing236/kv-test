# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoCap:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, create_mongo_instance):
        info_logger.info("[Scenario] Create an instance for mongo, the instance consists of a primary container, a secondary container and a hidden container")
        cluster_id = create_mongo_instance_step
        info_logger.info("[INFO] The mongo instance %s is created", cluster_id)

    @pytest.mark.smoke
    def _modify_name_for_mongo_instance(self, config, create_mongo_instance):
	info_logger.info("[Scenario] Modify name for the mongo instance")
	cluster_id = create_mongo_instance
	info_logger.info("[INFO] The mongo instance %s is created", cluster_id)
	modify_name_for_mongo_instance_step(cluster_id, space_name)
