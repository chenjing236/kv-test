# coding:utf-8
# from utils.HttpClient import *
import logging

logger_info = logging.getLogger(__name__)


class Container:
    def __init__(self, conf_obj, httpClient):
        self.conf_obj = conf_obj
        self.http_client = httpClient

    # 获取container信息，通过nova agent
    def get_container_info(self, nova_agent_host, container_id):
        status, headers, res_data = self.http_client.get_container_info(nova_agent_host + ":" + self.conf_obj["nova_agent_port"], container_id)
        if status == 404:
            assert False, "[ERROR] The container [{0}] on host [{1}] is not exist!".format(container_id, nova_agent_host)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 删除nova docker
    def delete_nova_docker(self, container_id):
        status = self.http_client.delete_nova_docker(container_id)
        assert status == 204, "[ERROR] HTTP Request of nova docker is failed, response is {0}".format(status)
        return True

    # stop nova docker
    def stop_nova_docker(self, container_id):
        status = self.http_client.stop_nova_docker(container_id)
        assert status == 202, "[ERROR] HTTP Request of nova docker is failed"
        return True
