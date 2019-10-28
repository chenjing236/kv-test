# coding=utf-8
from utils.SQLClient import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from steps.InstanceOperation import *
from steps.BillOperation import *

from logging.handlers import TimedRotatingFileHandler



def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="./config/conf_test_hd2.json", help="test config file path")
    parser.addoption("--loglevel", action="store", default=3, help="FATAL:0 ERROR:1")


#FATAL = 0 ERROR = 1 WARN = 2 INFO = 3
@pytest.fixture(scope="session", autouse=True)
def loglevel(request):
    return request.config.getoption("--loglevel")


@pytest.fixture(scope="session", autouse=True)
def config(request, loglevel):
    #load config
    file_path = request.config.getoption("config")
    conf_obj = json.load(open(file_path, 'r'))
    conf_obj["logger_level"] = loglevel
    #get account balance
    # before_account = get_account_balance(conf_obj["uc_url"], conf_obj["uc_token"])
    # conf_obj["before_account"] = before_account
    #load data
    data_obj =  json.load(open('./data/instance_data.json', 'r'))
    conf_obj.update(data_obj)
    return conf_obj


@pytest.fixture(scope="session")
def init_instance(config, request):
    client, resp, instance_id = create_instance(config)
    instance = None
    if resp.error is None and instance_id is not None:
        instance = query_instance_recurrent(200, 5, instance_id, config, client)
        config["request_id"] = resp.request_id
    else:
        config["request_id"] = ""
    def teardown():
        print "\n"
        time.sleep(300)
        if instance_id is not None:
            delete_instance(config, instance_id, client)

    request.addfinalizer(teardown)
    if instance is None:
        instance_id = None
    return client, resp, instance_id


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

