# -*- coding: utf-8 -*- 

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestSmokeCasesForMongoInstance:

    @pytest.mark.smoke
    def test_create_mongo_instance(self, create_mongo_instance):
	info_logger.info("[SCENARIO] Create a mongo instance that consists of a primary container, a secondary container and a hidden container")
        
