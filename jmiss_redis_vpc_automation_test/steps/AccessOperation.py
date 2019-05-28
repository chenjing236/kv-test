# coding:utf-8

from business_function.Accesser import *
import logging
info_logger = logging.getLogger(__name__)


# 验证space通过domain访问的正确性
def check_access_domain_step(accesser, space_id, password=None):
    info_logger.info("[STEP] Start to check[{0}] domain access, set/get key from domain".format(space_id))
    result = accesser.access_domain(space_id, password)
    assert result is True, info_logger.error("Check domain access failed, space_id is [{0}]".format(space_id))
    info_logger.info("Check domain access success!")
    return


# 验证space通过nlb访问的正确性
def check_access_nlb_step(accesser, space_id, password=None):
    info_logger.info("[STEP] Start to check[{0}] nlb access, set/get key from nlb".format(space_id))
    result = accesser.access_nlb(space_id, password)
    assert result is True, info_logger.error("Check nlb access failed, space_id is [{0}]".format(space_id))
    info_logger.info("Check nlb access success!")
    return


# 验证space通过所有ap访问的正确性
def check_access_ap_step(accesser, space_id, password=None):
    info_logger.info("[STEP] Start to check[{0}] ap access, set/get key from ap".format(space_id))
    result = accesser.access_ap(space_id, password)
    assert result is True, info_logger.error("Check ap access failed, space_id is [{0}]".format(space_id))
    info_logger.info("Check ap access success!")
    return


# 持续ping domain，直至域名生效
def ping_domain_step(accesser, space_id):
    info_logger.info("[STEP] Start to ping domain until domain is resolved")
    result = False
    err = None
    count = 1
    retry_times = accesser.conf_obj["retry_ping_domain_times"]
    wait_time = accesser.conf_obj["wait_time"]
    while result is False and count < retry_times:
        time.sleep(wait_time)
        result, err = accesser.ping_domain(space_id)
        count += 1
        # if unicode("未知的名称或服务") in err or "unknown host" in err:
        #     count += 1
        #     continue
        # else:
        #     print [result], err
        #     assert False, info_logger.error("Ping domain exec err, err msg is [{0}]".format(err))
    if count >= retry_times:
        assert False, info_logger.error("Ping domain exec over 60 times! It's not resolved!")
    if result is not True:
        assert False, info_logger.error("Ping domain of instance is failed, error_msg = {0}".format(err))
    info_logger.info("Ping domain of instance successfully")
    return True


# 验证space通过nlb执行配置文件中所有命令的正确性
