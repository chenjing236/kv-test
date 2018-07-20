# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)


# 验证space通过nlb访问的正确性
def check_access_nlb_step(accesser, space_id, password):
    logger_info.info("[INFO] Start to check[{0}] nlb access, set/get key from nlb".format(space_id))
    result = accesser.access_nlb(space_id, password)
    assert result is True, "[ERROR] Check nlb access failed, space_id is [{0}]".format(space_id)
    logger_info.info("[INFO] Check nlb access success!")
    return


# 验证space通过所有ap访问的正确性
def check_access_ap_step(accesser, space_id, password):
    logger_info.info("[INFO] Start to check[{0}] ap access, set/get key from ap".format(space_id))
    result = accesser.access_ap(space_id, password)
    assert result is True, "[ERROR] Check ap access failed, space_id is [{0}]".format(space_id)
    logger_info.info("[INFO] Check ap access success!")
    return


# 验证space通过nlb执行配置文件中所有命令的正确性
