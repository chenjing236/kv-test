# coding:utf-8
# from utils.HttpClient import *
import logging

info_logger = logging.getLogger(__name__)


class Container:
    def __init__(self, conf_obj, httpClient):
        self.conf_obj = conf_obj
        self.http_client = httpClient

    # 通过sagent获取当前ap docker中topo version
    def ping_ap_version(self, sagent_host, container_id, space_id):
        status, headers, res_data = self.http_client.ping_ap_version(sagent_host + ":1025", container_id, space_id)
        assert status == 200, "[ERROR] HTTP Request of sagent is failed, response is {0}".format(status)
        assert res_data["code"] == 0, "[ERROR] Ping ap version failed, msg is [{0}]".format(res_data["message"])
        return res_data

    # 获取container信息，通过nova agent
    def get_container_info(self, jcs_agent_host, container_id):
        status, headers, res_data = self.http_client.get_container_info(jcs_agent_host + ":" + self.conf_obj["jcs_agent_port"], container_id)
        assert status == 200, "[ERROR] HTTP Request of jcs eye is failed, response is {0}".format(status)
        assert res_data["code"] == 0, "[ERROR] The status of container is wrong, msg is [{0}]".format(res_data["detail"])
        return res_data

    # delete jcs docker
    def delete_jcs_docker(self, container_id):
        status, headers, res_data = self.http_client.delete_jcs_docker(container_id)
        assert status == 200, "[ERROR] HTTP Request of jcs docker is failed, response is {0}".format(status)
        assert res_data["code"] == 0, "[ERROR] Delete container failed, msg is [{0}]".format(res_data["detail"])
        return True

    # stop jcs docker
    def stop_jcs_docker(self, container_id):
        status, headers, res_data = self.http_client.stop_jcs_docker(container_id)
        assert status == 200, "[ERROR] HTTP Request of jcs docker is failed, status = {0}".format(status)
        assert res_data["code"] == 0, "[ERROR] Stop container failed, msg is [{0}]".format(res_data["detail"])
        return True
