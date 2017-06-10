# -*- coding: utf-8 -*- 

import pytest
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.HttpClient import *

logger_info = logging.getLogger(__name__)

#定义命令行参数
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="conf_test.json", help="test config file path")
    parser.addoption("--data", action="store", default="data_for_mongo_instance_test.json", help="data file path")

#获取环境配置信息
@pytest.fixture(scope="session", autouse=True)
def config(request):
    file_path = request.config.getoption("config")
    #file_path = cur_file_dir().replace("\\","/").replace("regression_cases", "") + "config/conf_test.json"
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj

#获取创建mongo单实例所需的数据信息
@pytest.fixture(scope="session", autouse=True)
def instance_data(request):
    file_path = request.config.getoption("data")
    #file_path = cur_file_dir().replace("\\","/").replace("regression_cases", "") + "config/data_for_mongo_instance_test.json"
    data_obj = json.load(open(file_path, 'r'))
    return data_obj

#创建http client对象
@pytest.fixture(scope="session")
def http_client(config):
    http_client = HttpClient(config["host"], config["cc_service_host"], config["pin"], config["token"], config["version"])
    return http_client

#日志
@pytest.fixture(scope="session", autouse=True)
def logger():
    info_logger = logging.getLogger()
    info_logger.setLevel(logging.DEBUG)

    failure_logger = logging.getLogger('failure')
    failure_logger.setLevel(logging.WARNING)

    stat_logger = logging.getLogger('stat')
    stat_logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")

    info_log_name = './REGRESSION_CLUSTER_DEBUG.log'
    info_file_handler = TimedRotatingFileHandler(info_log_name, 'midnight', 1, 31)
    info_file_handler.suffix="%Y-%m-%d.log"
    info_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setFormatter(formatter)

    info_stdout_handler = logging.StreamHandler(sys.stdout)
    info_stdout_handler.setLevel(logging.INFO)
    info_stdout_handler.setFormatter(formatter)

    failure_log_name = './FAILURE_CLUSTER_RECORD.log'
    failure_file_handler = logging.FileHandler(failure_log_name, 'a')
    failure_file_handler.setLevel(logging.WARNING)
    failure_file_handler.setFormatter(formatter)

    stat_log_name = './STAT_CLUSTER_RECORD.log' 
    stat_file_handler = logging.FileHandler(stat_log_name, 'a')
    stat_file_handler.setLevel(logging.INFO)
    stat_file_handler.setFormatter(formatter)
    info_logger.addHandler(info_file_handler)
    info_logger.addHandler(info_stdout_handler)
    failure_logger.addHandler(failure_file_handler)
    stat_logger.addHandler(stat_file_handler)
