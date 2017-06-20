# coding:utf-8
import logging

logger_info = logging.getLogger(__name__)

class Container:
    def __init__(self, conf_obj, docker_client):
        self.conf_obj = conf_obj
        self.docker_client = docker_client

    #获取container的memory size
    def get_memory_size_of_container(self, containerIp, containerPort):
        if self.docker_client == None:
            assert False, "[ERROR] Docker client is not initialized"
        memory_size = long(self.docker_client.get_container_mem_size(containerIp, containerPort)) / 1024
        return memory_size

    #获取container的disk size
    def get_disk_size_of_container(self, containerIp, containerPort):
	disk_size = get_container_disk_size(self, container_host, container_port)	
	return disk_size

    #获取container的count of cpu
    def get_cpu_count_of_container(self, containerIp, containerPort):
        logger_info.info("[TODO] get cpu count of container")

    #获取container的ipos
    def get_ipos_of_container(self, containerIp, containerPort):
        logger_info.info("[TODO] get ipos of container")

    #获取container的max connection
    def get_max_connection_count_of_container(self, containerIp, containerPort):
        logger_info.info("[TODO] get the count of max connecton of container")

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
