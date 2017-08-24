#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import logging
import time
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestBackupManually:
    '''
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

    '''
    @pytest.mark.smoke
    def test_backup_3(self,config,instance_data,http_client,mysql_client,create_mongo_instance):
        retry_times = int(config["retry_getting_info_times"])
        wait_time = int(config["wait_time"])
        info_logger.info("[SCENARIO] Generate a backup file for the mongo instance")
        space_id = create_mongo_instance
        # create an instance about mongo
        info_logger.info("[INFO] The instance of the mongo %s is created", space_id)
        #执行手动备份，备份3个状态为3的instance备份
        #count记录状态为3的备份数量
        count = 0
        rt = 0
        name = []
        while count < 3 and rt < retry_times:
            # generate a backup for the mongo
            operation_id = generate_backup_for_mongo_step(config, instance_data, http_client, space_id)
            ins = get_backup_info_step(config, instance_data, http_client, mysql_client, operation_id)
            rt = rt + 1
            if ins[0][1] == 3:
                count = count + 1
                name.append(ins[0][0])
            time.sleep(wait_time)
        assert count == 3,"[ERROR] We have tried {0} times, but we could not generate three backups,please check out".format(rt)
        #创建第四个状态为3的备份
        rt = 0
        while rt < retry_times:
            operation_id = generate_backup_for_mongo_step(config, instance_data, http_client, space_id)
            ins = get_backup_info_step(config, instance_data, http_client, mysql_client, operation_id)
            rt = rt + 1
            if ins[0][1] == 3:
                name.append(ins[0][0])
                break
            time.sleep(wait_time)
        assert len(name) == 4,"[ERROR] We have tried {0} times, but we could not generate the fourth backup,please check out".format(rt)
        # get list of finished backup
        total,first_backup = get_list_of_finished_backup_step(config, instance_data, http_client, space_id)
        retry_times = 15
        wait_time = 10
        count = 1
        while total > 3 and count < retry_times:
            time.sleep(wait_time)
            total, first_backup = get_list_of_finished_backup_step(config, instance_data, http_client, space_id)
        assert total < 4,"The spare backup is not deleted "
        assert total == 3,"Delete more than one backup"
        #查看第一个备份是否被删除
        assert first_backup["backupId"] != name[0],"[ERROR] The first backup is not deleted"


















