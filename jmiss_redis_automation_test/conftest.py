# coding=utf-8
from utils.SQLClient import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from steps.InstanceOperation import *

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
    #load data
    data_obj =  json.load(open('./data/instance_data.json', 'r'))
    conf_obj.update(data_obj)
    return conf_obj


@pytest.fixture(scope="session")
def init_instance(config, request):
    client, resp, instance_id = create_instance(config)

    if resp.error is None and instance_id is not None:
        query_instance_recurrent(200, 5, instance_id, config, client)
        config["request_id"] = resp.request_id
    else:
        config["request_id"] = ""
    def teardown():
        print "\n"
        time.sleep(30)
        if instance_id is not None:
            delete_instance(config, instance_id, client)

    request.addfinalizer(teardown)

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

    # formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    #
    # info_log_name = './REGRESSION_CLUSTER_DEBUG.log'
    # info_file_handler = TimedRotatingFileHandler(info_log_name, 'midnight', 1, 31)
    # info_file_handler.suffix = "%Y-%m-%d.log"
    # info_file_handler.setLevel(logging.DEBUG)
    # info_file_handler.setFormatter(formatter)
    #
    # info_stdout_handler = logging.StreamHandler(sys.stdout)
    # info_stdout_handler.setLevel(logging.INFO)
    # info_stdout_handler.setFormatter(formatter)
    #
    # failure_log_name = './FAILURE_CLUSTER_RECORD.log'
    # failure_file_handler = logging.FileHandler(failure_log_name, 'a')
    # failure_file_handler.setLevel(logging.WARNING)
    # failure_file_handler.setFormatter(formatter)
    #
    # stat_log_name = './STAT_CLUSTER_RECORD.log'
    # stat_file_handler = logging.FileHandler(stat_log_name, 'a')
    # stat_file_handler.setLevel(logging.INFO)
    # stat_file_handler.setFormatter(formatter)
    # info_logger.addHandler(info_file_handler)
    # info_logger.addHandler(info_stdout_handler)
    # failure_logger.addHandler(failure_file_handler)
    # stat_logger.addHandler(stat_file_handler)
