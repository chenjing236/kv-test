# coding:utf-8

from business_function.Accesser import *
import logging
import json
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
    return


# 验证通过域名执行redis unit test
def exec_unit_test_step(accesser, space_id):
    info_logger.info("[STEP] Start to exec redis unit test, space_id is [{0}]".format(space_id))
    info_logger.info("Exec redis unit test may take a few minutes, please wait for a while...")
    result = accesser.exec_unit_test(space_id)
    assert result is True, info_logger.error("Run redis unit test failed, please check vm error log")
    info_logger.info("Exec redis unit test successfully")
    return


# 通过域名写入测试数据，数据分布在0-511 slots上
def insert_test_keys(accesser, space_id, password=None):
    info_logger.info("[STEP] Start to insert redis test keys which include slot [0-511], space_id is [{0}]".format(space_id))
    info_logger.info("Insert keys may take a few seconds, please wait for a while...")
    set_result = accesser.exec_slot_keys(space_id, "set", password)
    assert set_result is True, info_logger.error("Set key value failed!")
    info_logger.info("Insert redis test keys successfully!")
    return


# 通过域名读取测试数据，数据分布在0-511 slots上
def query_test_keys(accesser, space_id, password=None):
    info_logger.info("[STEP] Start to query redis test keys which include slot [0-511], space_id is [{0}]".format(space_id))
    info_logger.info("Query keys may take a few seconds, please wait for a while...")
    get_result = accesser.exec_slot_keys(space_id, "get", password)
    assert get_result is True, info_logger.error("Get key value failed!")
    info_logger.info("Query redis test keys successfully!")
    return
