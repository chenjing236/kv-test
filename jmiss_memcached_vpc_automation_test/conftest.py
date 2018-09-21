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
def create_instance(config):
    client = setClient(config)
    header = getHeader(config)
    instance_id = None
    resp = dict()
    name = "auto_test_" + str(int(time.time()))
    try:
        charge = ChargeSpec('postpaid_by_duration', 'year', 1)
        instance = InstanceSpec('MC-S-1C1G', 'single', config["az"],
                                config["vpc"], config["subnet"], name,
                                config["version"], True, charge, "desc", "12345678")
        parameters = CreateInstanceParameters(config["region"], instance)
        request = CreateInstanceRequest(parameters, header)
        resp = client.send(request)
    except Exception, e:
        print e

    if resp.error is None:
        instance = query_instance_recurrent(100, 6, name, config)
        if instance is not None:
            instance_id = instance["instances"][0]["instanceId"]

    return client, resp, name, instance_id



@pytest.fixture(scope="session")
def sql_client(config):
    sql_cli = SQLClient(config["mysql_host"],
                        config["mysql_port"],
                        config["mysql_user"],
                        config["mysql_passwd"],
                        config["mysql_db"])
    return sql_cli

