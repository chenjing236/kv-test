#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestBackupManually:
    @pytest.mark.smoke
    def test_backup_manually(self,config,instance_data,http_client,mysql_client,create_mongo_instance):
        info_logger.info("[SCENARIO] Generate a backup file for the mongo instance")
        space_id = create_mongo_instance
        #create an instance about mongo
        info_logger.info("[INFO] The instance of the mongo %s is created",space_id)
        #generate a backup for the mongo
        operation_id = generate_backup_for_mongo_step(config,instance_data,http_client,space_id)
        #get list of backup
        total,backup_list = get_list_of_backup_step(config,instance_data,http_client,space_id)
        assert total == 1,"The number of total is incorrect"
        assert backup_list[0]['status'] == 'Finished',"[ERROR] The backup of the instance is not completed"
        #get the backup of the instance in table backup
        ins = get_backup_info_step(config,instance_data,http_client,mysql_client,operation_id)
        assert ins[0][1] == 3, "[ERROR] The backup info is incompleted"
        name = ins[0][0]
        assert backup_list[0]['backupId'] == name,"[ERROR] The backup in sql is not the same"
