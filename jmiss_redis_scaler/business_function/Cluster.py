# coding:utf-8
import json
import string
import random


# 缓存云实例类
class Cluster(object):
    def __init__(self, httpClient, sqlClient, config):
        self.httpClient = httpClient
        self.sqlClient = sqlClient
        self.conf_obj = config

    # upgrade ap
    def upgrade_instance_ap(self, space_id, image_tag):
        data = {"upgradeType": 2, "spaceId": space_id, "imageTag": image_tag, "migrateFlag": 0}
        status, headers, res_data = self.httpClient.upgrade_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # upgrade redis
    def upgrade_instance_redis(self, space_id, image_tag, migrate_flag=0):
        data = {"upgradeType": 1, "spaceId": space_id, "imageTag": image_tag, "migrateFlag": migrate_flag}
        status, headers, res_data = self.httpClient.upgrade_cluster(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
