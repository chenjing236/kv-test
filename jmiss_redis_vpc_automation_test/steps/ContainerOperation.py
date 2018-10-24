# coding:utf-8
from business_function.Container import *
import logging
info_logger = logging.getLogger(__name__)


# 调用jcs-eye接口获取docker信息
def get_container_info_step(container, jcs_agent_host, container_id):
    info_logger.info("[STEP] Get container info from jcs eye")
    res_data = container.get_container_info(jcs_agent_host, container_id)
    if res_data["data"] is None or res_data["data"] is "":
        assert False, info_logger.error("Response of get_container_info is incorrect for the container {0}".format(container_id))
    assert res_data["data"]["state"] == "running", info_logger.error("The state of container[{0}] is not running, its state is {1}".format(container_id, res_data["data"]["state"]))
    info_logger.info("Memory size of container[{0}] is {1}".format(container_id, res_data["data"]["mem_total"]))
    return res_data["data"]["mem_total"]


# 调用jcs接口删除jcs docker
def delete_jcs_docker_step(container, container_id):
    return container.delete_jcs_docker(container_id)


# 调用jcs接口stop jcs docker
def stop_jcs_docker_step(container, container_id):
    return container.stop_jcs_docker(container_id)
