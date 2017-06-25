# coding:utf-8
import logging

logger_info = logging.getLogger(__name__)

class Container:
    def __init__(self, conf_obj, http_client, docker_client):
        self.conf_obj = conf_obj
	self.http_client = http_client
        self.docker_client = docker_client

    #通过nova agent获取container信息
    def get_container_info(self, container_info):
	mongo_agent_host=container_info["host_ip"] + ":" + self.config["mongo_agent_port"]
	status, headers, res_data = self.http_client.get_container_info(mongo_agent_host, container_info["docker_id"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #通过mongo agent ping mongo的container，验证mongo的container是否存在及是否存活
    def ping_container(self, container_info):
        mongo_agent_host=container_info["host_ip"] + ":" + self.conf_obj["mongo_agent_port"]
        status, headers, res_data = self.http_client.ping_container_of_mongo_instance(mongo_agent_host, container_info["docker_id"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #通过mongo agent 获取mongo的副本集关系
    def get_replica_info_from_container(self, container_info):
        mongo_agent_host=container_info["host_ip"] + ":" + self.conf_obj["mongo_agent_port"]
        status, headers, res_data = self.http_client.get_replic_info_from_container(mongo_agent_host, container_info["docker_id"])
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
