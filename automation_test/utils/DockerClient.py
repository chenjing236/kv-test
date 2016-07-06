#!/usr/bin/python
# coding:utf-8
from docker import Client
import json
import time


class DockerClient(object):
    def __init__(self, docker_daemon_port, docker_version):
        self.docker_daemon_port = docker_daemon_port
        self.docker_version = docker_version

    def stop_container(self, container_host, container_port):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        container_name = "{0}_{1}".format(container_host, container_port)
        print "begin to start container:{0}".format(container_name)
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name}, all=True)
        if len(ret_containers) < 1:
            print "can't find container:[{0}]".format(container_name)
            return False
        print ret_containers[0]
        container_status = ret_containers[0]["Status"]
        if container_status.startswith("Up "):
            c.stop(container_name)
        else:
            print "Status of container:{0} isn't up: [{1}]".format(container_name, container_status)
            return False
        print "stop container:{0} successed".format(container_name)
        return True

    def remove_container(self, container_host, container_port):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        container_name = "{0}_{1}".format(container_host, container_port)
        print "begin to remove container:{0}".format(container_name)
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name})
        if len(ret_containers) < 1:
            print "remove container failed! can't find container:[{0}]".format(container_name)
            return False
        print ret_containers[0]
        container_status = ret_containers[0]["Status"]
        if container_status.startswith("Up "):
            c.stop(container_name)
        c.remove_container(container_name)
        print "remove container:{0} success".format(container_name)
        return True

        #c.stop(container_name)

    #    def init(self,ip,docker_daemon_port):
    #        docker_server = "tcp://{0}:{1}".format(ip,docker_daemon_port)
    #        return Client(base_url=docker_server,version=self.docker_version)

    # 停止缓存云实例的slave
    # 参数
    #   slef
    #   slave_ip,slave所在Docker的服务器IP
    #   slave_port,slave对应的PORT
    #   docker_daemon_port,slave所在Docker的守护进程的PORT
    def stop_slave(self, space_id, slave_ip, slave_port, docker_daemon_port):
        slave_ip_port = "{0}_{1}".format(slave_ip,slave_port)
        # 链接docker服务器的守护进程，根据IP_PORT停止slave
        docker_server = "tcp://{0}:{1}".format(slave_ip, docker_daemon_port)
        c = Client(base_url=docker_server, version=self.docker_version)
        # 获取当前slave所有的containers
        containers = list(c.containers())
        for container in containers:
            container_json = json.dumps(container)
            decodejson = json.loads(container_json)
            container_ip_port = "{0}".format(decodejson["Names"][0])
            if slave_ip_port in container_ip_port:
                container_id = decodejson["Id"]
                container_status = decodejson["Status"]
                print "[ACTION] Stop slave of cache instance (space_id={0}). Slave Info : Container ID : Container Status={1}:{2}".format(
                    space_id, container_id, container_status)
                # stop slave
                c.stop(container_id)
                c.remove_container(container_id)
                time.sleep(2)

        c.close()

    # 停止缓存云实例的master
    # 参数
    #   slef
    #   master_ip,master所在Docker的服务器IP
    #   master_port,master对应的PORT
    #   docker_daemon_port,slave所在Docker的守护进程的PORT
    def stop_master(self, space_id, master_ip, master_port, docker_daemon_port):
        '''
            :param slave_ip,slave_port,docker_daemon_port:
            :return: []
        '''
        master_ip_port = "/{0}".format(master_ip) + "_" + "{0}".format(master_port)
        # 链接docker服务器的守护进程，根据IP_PORT停止slave
        docker_server = "tcp://{0}:{1}".format(master_ip, docker_daemon_port)
        c = Client(base_url=docker_server, version=self.docker_version)
        # 获取当前slave所有的containers
        containers = list(c.containers())
        for container in containers:
            container_json = json.dumps(container)
            decodejson = json.loads(container_json)
            container_ip_port = "{0}".format(decodejson["Names"][0])
            if master_ip_port in container_ip_port:
                container_id = decodejson["Id"]
                container_status = decodejson["Status"]
                print "[ACTION] Stop master of cache instance （space_id={0}）. Master Info : Container ID : Container Status={1}:{2}".format(
                    space_id, container_id, container_status)
                # stop slave
                c.stop(container_id)
                c.remove_container(container_id)
                time.sleep(2)

        c.close()


