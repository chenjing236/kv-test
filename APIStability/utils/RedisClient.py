#!/usr/bin/python
# coding:utf-8
import redis
from docker import Client
from JCacheUtils import *
import json

class RedisClient(object):
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj
        self.docker_daemon_port = self.conf_obj["docker_daemon_port"]
        self.docker_version = self.conf_obj["docker_version"]

    def redis_client(self, capacity, container_host, container_port):
        container_name = "{0}_{1}".format(container_host, container_port)
        info_logger.info("check redis memory: begin to check redis client:{0}".format(container_name))
        # redis client
        r = redis.StrictRedis(container_host, container_port)
        # redis maxmemory
        mm = r.config_get("maxmemory")
        info_logger.info("check redis memory: config_get maxmemory info={0}".format(mm))
        maxmemory = int(mm['maxmemory'])
        # check maxmemory
        if capacity != maxmemory:
            info_logger.error("check redis memory: check redis memory error! capacity={0}, maxmemory={1}".format(capacity, maxmemory))
            return False
        info_logger.info("check redis memory: check redis memory success!")
        return True
