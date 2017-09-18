# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)


# 调用nova接口获取docker信息
def get_container_info_step(container, nova_agent_host, container_id):
    res_data = container.get_container_info(nova_agent_host, container_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_container_info is incorrect for the container {0}".format(container_id)
    return res_data["memInfo"]


# 调用nova接口删除nova docker
def delete_nova_docker_step(container, container_id):
    return container.delete_nova_docker(container_id)


# 调用nova接口stop nova docker
def stop_nova_docker_step(container, container_id):
    return container.stop_nova_docker(container_id)
