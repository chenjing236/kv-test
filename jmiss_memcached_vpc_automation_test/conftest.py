# coding=utf-8
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.memcached.client.MemcachedClient import *
import time
from utils.SQLClient import *
import json
import pytest
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *
from logging.handlers import TimedRotatingFileHandler



def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="conf.json", help="test config file path")
    parser.addoption("--data", action="store", default="instance_data.json", help="data file path")


@pytest.fixture(scope="session", autouse=True)
def config(request):
    file_path = request.config.getoption("config")
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj


@pytest.fixture(scope="session")
def instance_data(request):
    file_path = request.config.getoption("data")
    data = json.load(open(file_path, 'r'))
    return data


@pytest.fixture(scope="session")
def create_instance(config, request):
    client = setClient(config)
    header = getHeader(config)
    instance_id = None
    resp = dict()
    name = "auto_test_" + str(int(time.time()))
    try:
        charge = ChargeSpec('postpaid_by_duration', 'year', 1)
        instance = InstanceSpec('MC-S-1C1G', 'single', config["az"],
                                config["vpc"], config["subnet"], name,
                                config["version"], True, "desc", "12345678", charge)
        parameters = CreateInstanceParameters(config["region"], instance)
        req = CreateInstanceRequest(parameters, header)
        resp = client.send(req)
    except Exception, e:
        print e

    if resp.error is None:
        instance = query_instance_recurrent(160, 6, name, config)
        if instance is not None:
            instance_id = instance["instances"][0]["instanceId"]

    def teardown():
        print "\n"
        deleteInstance(client, instance_id, config)
        time.sleep(15)

    request.addfinalizer(teardown)

    return client, resp, name, instance_id



@pytest.fixture(scope="session")
def sql_client(config):
    sql_cli = SQLClient(config["mysql_host"],
                        config["mysql_port"],
                        config["mysql_user"],
                        config["mysql_passwd"],
                        config["mysql_db"])
    return sql_cli


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
    info_file_handler.suffix = "%Y-%m-%d.log"
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
