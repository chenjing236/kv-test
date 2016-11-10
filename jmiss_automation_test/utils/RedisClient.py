#!/usr/bin/python
# coding:utf-8
import redis
import time
import json

class RedisClient(object):
    def __init__(self, redisHost, redisPort, password):
        self.redisHost = redisHost
        self.redisPort = redisPort
        self.password = password
        self.container_cnt = redis.StrictRedis(host=redisHost, port=redisPort)
        self.ap_cnt = redis.StrictRedis(host=redisHost, port=redisPort, password=password)

    def check_redis_instances(self, instances):
        master = instances[0]
        slave = instances[1]
        cnt = redis.StrictRedis(host=master[0], port=master[1])
        cnt.set("test", "test_str")
        assert cnt.get("test") == "test_str"
        time.sleep(1)
        cnt_slave = redis.StrictRedis(host=slave[0], port=slave[1])
        assert cnt_slave.get("test") == "test_str"
        cnt.delete('test')
        assert cnt_slave.get("test") is None

    def get_value(self, redisInfo, key):
        cnt_redis = redis.StrictRedis(host=redisInfo[0], port=redisInfo[1])
        time.sleep(1)
        return cnt_redis.get(key)

    def set_key_value(self, master,key,value):
        cnt = redis.StrictRedis(host=master[0], port=master[1])
        cnt.set(key, value)
        time.sleep(1)

    def set_key_value_for_master(self, masterIp, masterPort, key,value):
        cnt = redis.StrictRedis(host=masterIp, port=masterPort)
        cnt.set(key, value)
        time.sleep(1)

    def get_value_from_slave(self, slaveIp, slavePort, key):
        cnt_redis = redis.StrictRedis(host=slaveIp, port=slavePort)
        time.sleep(1)
        return cnt_redis.get(key)

    def delete_key_value(self, master,key):
        cnt = redis.StrictRedis(host=master[0], port=master[1])
        cnt.delete(key)
        time.sleep(1)

    def access_ap_and_operate_key(self, ap_host, ap_port, passwd, jinstance):
        cnt = redis.StrictRedis(host=ap_host, port=ap_port, password=passwd)
        cnt.set("test_ap", "test_ap_value")
        assert cnt.get("test_ap") == "test_ap_value"
        cnt_ins = redis.StrictRedis(host=jinstance[0], port=jinstance[1])
        assert cnt_ins.get("test_ap") == "test_ap_value"

    def check_ap_access(self, ap_host, ap_port, passwd):
        try:
            cnt = redis.StrictRedis(host=ap_host, port=ap_port, password=passwd)
        except redis.ConnectionError:
            assert False, "[ERROR] Cannot access to AP with the password {0}".format(passwd)
        print "[INFO] Set key:value {test_ap:test_ap_value}"
        try:
            cnt.set("test_ap", "test_ap_value")
        except redis.ConnectionError:
            assert False, "[ERROR] Cannot set key: value with AP"
        try:
            value = cnt.get("test_ap")
        except redis.ConnectionError:
            assert False, "[ERROR] Cannot get value by the key {0}".format("test_ap")
        assert value  == "test_ap_value"
        print "[INFO] Get key:value {test_ap:test_ap_value}"
        return True

    def get_redis_info(self, redis_host, redis_port):
        cnt = redis.StrictRedis(host=redis_host, port=redis_port)
        info = cnt.info()
        if len(info) < 1:
            raise Exception("[ERROR] Cannot get information for redis({0}:{1})").format(redis_host,redis_port)

        redis_info = json.loads(json.dumps(info).replace("'","\""))
        return redis_info

    def get_value_from_ap_by_key(self, ap_host, ap_port, passwd, key):
        try:
            cnt = redis.StrictRedis(host=ap_host, port=ap_port, password=passwd)
        except redis.ConnectionError:
            assert False, "[ERROR] Cannot access to AP with the password {0}".format(passwd)
        try:
            value = cnt.get(key)
        except redis.ConnectionError:
            assert False, "[ERROR] Cannot get value by the key {0}".format(key)
        return value

