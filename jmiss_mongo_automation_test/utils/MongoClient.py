# -*- coding: utf-8 -*- 

from pymongo import *
import logging

logger_info = logging.getLogger(__name__)

# 通过UDS连接mongo实例的container中的mongo服务
class MongoClient(object):
    def __init__(self, mongoHost, mongoRst, mongoPort, user, password):
        self.mongoHost = mongoHost
        self.mongoPort = mongoPort
	self.user = user
        self.password = password

    #通过UDS访问mongo的container
    def init_connection_with_mongo(self, user, password, sockFilePath):
	uds_connection_url = "mongodb://" + user + ":" + password + "@" + sockFilePath
	logger_info.info("[INFO] The url for uds is %s", uds_connection_url)
	client = MongoClient(uds_connection_url)
	return client

    def get_config_of_container(self, client):
	logger_info.info("[INFO] Get the container info using uds")
