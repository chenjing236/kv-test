#!/usr/bin/python
# coding:utf-8
#import sys
#sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/utils")
from DockerClient import *
import json
import time

class Container:
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj
        self.docker_client = DockerClient(self.conf_obj)

    #获取container的memory size
    def get_memory_size_of_container(self, containerIp, containerPort):
        if self.docker_client == None:
            assert False, "[ERROR] Docker client is not initialized"
        memory_size = long(self.docker_client.get_container_mem_size(containerIp, containerPort)) / 1024
        return memory_size

    #获取container的创建时间
    def get_creation_time_of_container(self, containerIp, containerPort):
        if self.docker_client == None:
            assert False, "[ERROR] Docker client is not initialized"
        creation_time = self.docker_client.get_creation_time_of_container(containerIp, containerPort)
        return creation_time

    #failover master container or failover slave container
    def stop_container(self, containerIp, containerPort):
        if self.docker_client == None:
            assert False, "[ERROR] Docker client is not initialized"
        is_stopped = self.docker_client.stop_container(containerIp, containerPort)
        assert is_stopped == True, "Container {0}:{1} is stopped".format(containerIp, containerPort)