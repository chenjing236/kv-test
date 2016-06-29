#!/usr/bin/python
#coding:utf-8
from utils.tools import *
from docker import Client
import json
import string
import time

class DockerClient(object):
    def __init__(self,conf_path):
        self.conf_path = conf_path
        self.conf_obj = json.load(open(conf_path, 'r'))
        self.container_daemon = self.conf_obj['docker_daemon']
        self.docker_version = self.conf_obj['docker_version']

#    def init(self,ip,container_daemon):
#        docker_server = "tcp://{0}:{1}".format(ip,container_daemon)
#        return Client(base_url=docker_server,version=self.docker_version)

    #停止缓存云实例的slave
    #参数
    #   slef
    #   slave_ip,slave所在Docker的服务器IP
    #   slave_port,slave对应的PORT
    #   container_daemon,slave所在Docker的守护进程的PORT
    def stop_slave(self,space_id,slave_ip,slave_port,container_daemon):
        '''
            :param slave_ip,slave_port,container_daemon:
            :return: []
        '''
        slave_ip_port = "/{0}".format(slave_ip) + "_" + "{0}".format(slave_port)
        #链接docker服务器的守护进程，根据IP_PORT停止slave
        docker_server = "tcp://{0}:{1}".format(slave_ip,container_daemon)
        c = Client(base_url=docker_server,version=self.docker_version)
        #获取当前slave所有的containers
        containers = list(c.containers())
        for container in containers:
            container_json = json.dumps(container)
            decodejson = json.loads(container_json)
            container_ip_port = "{0}".format(decodejson["Names"][0])
            if slave_ip_port in container_ip_port:
                container_id = decodejson["Id"]
                container_status = decodejson["Status"]
                print "[ACTION] Stop slave of cache instance (space_id={0}). Slave Info : Container ID : Container Status={1}:{2}".format(space_id,container_id,container_status)
                #stop slave
                c.stop(container_id)
                c.remove_container(container_id)
                time.sleep(2)

        c.close()

    #停止缓存云实例的master
    #参数
    #   slef
    #   master_ip,master所在Docker的服务器IP
    #   master_port,master对应的PORT
    #   container_daemon,slave所在Docker的守护进程的PORT
    def stop_master(self,space_id,master_ip,master_port,container_daemon):
        '''
            :param slave_ip,slave_port,container_daemon:
            :return: []
        '''
        master_ip_port = "/{0}".format(master_ip) + "_" + "{0}".format(master_port)
        #链接docker服务器的守护进程，根据IP_PORT停止slave
        docker_server = "tcp://{0}:{1}".format(master_ip,container_daemon)
        c = Client(base_url=docker_server,version=self.docker_version)
        #获取当前slave所有的containers
        containers = list(c.containers())
        for container in containers:
            container_json = json.dumps(container)
            decodejson = json.loads(container_json)
            container_ip_port = "{0}".format(decodejson["Names"][0])
            if master_ip_port in container_ip_port:
                container_id = decodejson["Id"]
                container_status = decodejson["Status"]
                print "[ACTION] Stop master of cache instance （space_id={0}）. Master Info : Container ID : Container Status={1}:{2}".format(space_id,container_id,container_status)
                #stop slave
                c.stop(container_id)
                c.remove_container(container_id)
                time.sleep(2)

        c.close()