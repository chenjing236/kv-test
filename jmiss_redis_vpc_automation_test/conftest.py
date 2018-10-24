# coding=utf-8
import pytest
from utils.HttpClient import *
from steps.ClusterOperation import *
from steps.ContainerOperation import *
from steps.AccessOperation import *
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from logging.handlers import TimedRotatingFileHandler

# info_logger = logging.getLogger(__name__)


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
def created_instance(config, instance_data, http_client, request):
    instance = Cluster(config, instance_data, http_client)
    space_id, operation_id, password = create_instance_step(instance)
    # 查看创建操作结果，验证创建成功
    get_operation_result_step(instance, space_id, operation_id)
    # 设置资源acl
    set_acl_step(instance, space_id)

    def teardown():
        print "\n"
        info_logger.info("[TEARDOWN] Delete the instance {0}".format(space_id))
        instance.delete_instance(space_id)
        time.sleep(15)

    request.addfinalizer(teardown)
    return space_id, instance, password


@pytest.fixture(scope="session")
def http_client(config):
    http_cli = HttpClient(config["host"], config["pin"], config["auth_token"], config["version"], config["tenant_id"], config["jcs_docker_host"], config["user"])
    return http_cli


@pytest.fixture(scope="session")
def docker_client(config):
    docker_cli = Container(config)
    return docker_cli


@pytest.fixture(scope="session")
def sql_client(config):
    sql_cli = SQLClient(config["mysql_host"], config["mysql_port"], config["mysql_user"], config["mysql_passwd"], config["mysql_db"])
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
