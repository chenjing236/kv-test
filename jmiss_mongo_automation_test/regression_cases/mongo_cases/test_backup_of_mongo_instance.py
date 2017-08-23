#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestBackupManually:
    @pytest.mark.smoke
    def test_backup_manually(self,config,instance_data,http_client,create_mongo_instance):
        info_logger.info("[SCENARIO] Generate a backup file for the mongo instance")
        space_id = create_mongo_instance
        #create an instance about mongo
        info_logger.info("[INFO] The instance of the mongo %s is created",space_id)
        #generate a backup for the mongo
        operation_id = generate_backup_for_mongo_step(config,instance_data,http_client,space_id)
        #get list of backup
        backup_list = get_list_of_backup_step(config,instance_data,http_client,space_id)