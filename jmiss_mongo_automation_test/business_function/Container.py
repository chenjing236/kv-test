# coding:utf-8
import logging

logger_info = logging.getLogger(__name__)

class Container:
    def __init__(self, conf_obj, http_client, docker_client):
        self.conf_obj = conf_obj
	self.http_client = http_client
        self.docker_client = docker_client

    #通过nova agent获取container信息
    def get_container_info(self, nova_agent_host, nova_container_id):
	print "================================== {0}, {1}".format(nova_agent_host, nova_container_id)
	status, headers, res_data = self.http_client.get_container_info(nova_agent_host, nova_container_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
