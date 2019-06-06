# coding:utf-8

from business_function.Accesser import *
from utils.util import get_key_slot_list
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
    key_slot_list = get_key_slot_list()
    for key_slot in key_slot_list:
        set_result = accesser.domain_exec_command(space_id, " -n 2 set {0} {1}".format(key_slot[0], key_slot[1]), password)
        set_result = set_result[0].replace("\r", "").replace("\n", "")
        assert set_result == "OK", info_logger.error("Set key value error! Err result is {0}".format(set_result))
    info_logger.info("Exec redis unit test successfully")
    return

file_path = "../config/conf_test_02.json"
conf_obj = json.load(open(file_path, 'r'))
accesser = Accesser(conf_obj)
insert_test_keys(accesser, "redis-uvn3wehsu7")
