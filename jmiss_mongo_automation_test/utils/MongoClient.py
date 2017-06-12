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
	self.client = init_connection_with_mongo(user, password, sockFilePath)

    def init_connection_with_mongo(self, user, password, sockFilePath):
	uds_connection_url = "mongodb://" + user + ":" + password + "@" + sockFilePath
	#client = MongoClient("mongodb://root:1qaz2WSX@%2fmnt%2fb44f24ec-bb08-4f7a-947d-a06d00e04c5d%2fmongodb-27017.sock")
	client = MongoClient(uds_connection_url)
	return client
