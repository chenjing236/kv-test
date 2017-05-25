#!/usr/bin/env python
# coding:utf-8
import sys
import math
from pymongo import *

def main():
    print "[=== [START] insert data into mongo db ===]"
    client = MongoClient("mongodb://root:1qaz2WSX@%2fmnt%2fb44f24ec-bb08-4f7a-947d-a06d00e04c5d%2fmongodb-27017.sock")
    db = client.test_mongo
    collection = db.mongo_collection
    for i in range(1,999999):
    	data = {"id":i, "name":"mongo", "version":"3.2.9", "database":"test_mongo", "collection":"mongo_collection", "function":"测试断点续传"}
	collection.insert(data)
	data = {"id":i, "name":"redis", "version":"3.2.9", "database":"test_redis", "collection":"redis_collection", "function":"写入数据，测试断点续传"}
	collection.insert(data)
	print "[=== [END] ===]"

if __name__ == '__main__':
	sys.exit(main())

