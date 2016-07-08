#!/usr/bin/python
# coding:utf-8
from docker import Client
import json

class DockerClient(object):
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj
        self.docker_daemon_port = self.conf_obj["docker_daemon_port"]
        self.docker_version = self.conf_obj["docker_version"]

    def stop_container(self, container_host, container_port):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        container_name = "{0}_{1}".format(container_host, container_port)
        print "[ACTION] Begin to stop container:{0}".format(container_name)
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name}, all=True)
        if len(ret_containers) < 1:
            print "[ERROR] Can't find container:[{0}]".format(container_name)
            return False
        print "[INFO] Containers info={0}".format(json.dumps(ret_containers[0]))
        container_status = ret_containers[0]["Status"]
        container_id =  ret_containers[0]["Id"]
        if container_status.startswith("Up "):
            c.stop(container_name)
            c.remove_container(container_id)
        else:
            print "[INFO] Status of container:{0} isn't up: [{1}]".format(container_name, container_status)
            return False
        print "[INFO] Stop container:{0} successed".format(container_name)
        return True

    def remove_container(self, container_host, container_port):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        container_name = "{0}_{1}".format(container_host, container_port)
        print "[ACTION] Begin to remove container:{0}".format(container_name)
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name})
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
        print "[INFO] Remove container:{0} success".format(container_name)
        return True

