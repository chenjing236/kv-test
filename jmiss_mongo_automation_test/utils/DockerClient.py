#!/usr/bin/python
# coding:utf-8
from docker import Client
import json
import sys

class DockerClient(object):
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj
        self.docker_version = self.conf_obj["docker_version"]

    def init_docker_client(self, container_host):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        return Client(base_url=base_url, version=self.docker_version)

    def get_specific_container(self, docker_client, container_name):
        return docker_client.containers(filters={"name": container_name}, all=True)

    def get_container_name(self, container_host, container_port):
        return "{0}_{1}".format(container_host, container_port)

    #暂停container
    def stop_container(self, container_host, container_port):
        c = self.init_docker_client(container_host)
        container_name = self.get_container_name(container_host, container_port)
        ret_containers = self.get_specific_container(c, container_name)
        if len(ret_containers) < 1:
            print "[ERROR] Cannot find container:[{0}]".format(container_name)
            return False
        container_status = ret_containers[0]["Status"]
        container_id =  ret_containers[0]["Id"]
        if container_status.startswith("Up "):
            c.stop(container_name)
            c.remove_container(container_id)
        else:
            print "[INFO] Status of the container {0} isn't up: [{1}]".format(container_name, container_status)
            return False
        print "[INFO] It is successful to stop the container {0}".format(container_name)
        return True

    #删除container
    def remove_container(self, container_host, container_port):
        c = self.init_docker_client(container_host)
        container_name = self.get_container_name(container_host, container_port)
        ret_containers = self.get_specific_container(c, container_name)
        if len(ret_containers) < 1:
            print "[ERROR] Remove container failed! can't find container:[{0}]".format(container_name)
            return False
        print ret_containers[0]
        container_status = ret_containers[0]["Status"]
        container_id =  ret_containers[0]["Id"]
        if container_status.startswith("Up "):
            c.stop(container_name)
            c.remove_container(container_id)
        c.remove_container(container_name)
        print "[INFO] It is successful to remove the container {0}".format(container_name)
        return True

    #获取container的memory size
    def get_container_mem_size(self, container_host, container_port):
        docker_client = self.init_docker_client(container_host)
        container_name = self.get_container_name(container_host, container_port)
        container = self.get_specific_container(docker_client, container_name)[0]
        if container == None:
            print "[ERROR] There is no container"
            return None
        docker_inspect = docker_client.inspect_container(container)
        if docker_inspect == None:
            print "[ERROR] There is no inspecting information"
            return None
        docker_container_config = docker_inspect["HostConfig"]
        container_memory_size = docker_container_config["Memory"]
        return container_memory_size

    #获取container的memory size
    def get_container_disk_size(self, container_host, container_port):
        docker_client = self.init_docker_client(container_host)
        container_name = self.get_container_name(container_host, container_port)
        container = self.get_specific_container(docker_client, container_name)[0]
        if container == None:
            print "[ERROR] There is no container"
            return None
        docker_inspect = docker_client.inspect_container(container)
        if docker_inspect == None:
            print "[ERROR] There is no inspecting information"
            return None
        docker_container_config = docker_inspect["HostConfig"]
        container_disk_size = docker_container_config["Disk"]
        return container_disk_size

    #获取container的创建时间
    def get_creation_time_of_container(self, container_host, container_port):
        docker_client = self.init_docker_client(container_host)
        container_name = self.get_container_name(container_host, container_port)
        container = self.get_specific_container(docker_client, container_name)[0]
        if container == None:
            print "[ERROR] There is no container"
            return None
        docker_inspect = docker_client.inspect_container(container)
        if docker_inspect == None:
            print "[ERROR] There is no inspecting information"
            return None
        creation_time = docker_inspect["Created"]
        return creation_time

