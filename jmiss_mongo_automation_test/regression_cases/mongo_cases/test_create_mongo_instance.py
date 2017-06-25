# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestCreateMongoInstance:

    # 创建不同规格的mongo实例，验证实际mongo对应的container的规格与创建时指定的规格一致
    @pytest.mark.smoke
    def _create_mongo_instance_and_verify_flavor(self, config, instance_data, http_client, mysql_client, docker_client):
        info_logger.info("[SCENARIO] Create two mongo instances whith different flavors")

    #创建mongo实例，验证mongo实例创建成功后，数据库中的信息正确	
    def _create_mongo_instance_and_verify_data(self, config, instance_data, http_client, mysql_client,):
	info_logger.info("[SCENARIO] Create a mongo instance and verify that the data of the mongo created is correct")

