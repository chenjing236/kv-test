# coding=utf-8
import pytest
from utils.HttpClient import *
from utils.util import *
from steps.RedisOperationSteps import *
from steps.ClusterOperation import *
from steps.ContainerOperation import *
from steps.AccessOperation import *
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from logging.handlers import TimedRotatingFileHandler
import logging
info_logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="conf.json", help="test config file path")
    parser.addoption("--data", action="store", default="instance_data.json", help="data file path")


@pytest.fixture(scope="function", autouse=True)
def log_return(request):
    print

    def teardown():
        print
    request.addfinalizer(teardown)


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


# @pytest.fixture(scope="function")
# def get_create_params(instance_data):
#     create_params = {
#         "cacheInstanceName": instance_data["cache_instance_name"],
#         "cacheInstanceDescription": instance_data["cache_instance_description"],
#         "password": instance_data["password"],
#         "cacheInstanceClass": instance_data["cache_instance_class"],
#         "vpcId": instance_data["vpc_id"],
#         "subnetId": instance_data["subnet_id"],
#         "azId": {
#             "master": instance_data["master_az_id"],
#             "slave": instance_data["slaver_az_id"]
#         },
#         "redisVersion": "2.8"
#     }
#     charge_params = {
#         "chargeDuration": instance_data["charge_duration"],
#         "chargeMode": instance_data["charge_mode"],
#         "chargeUnit": instance_data["charge_unit"]
#     }
#     return create_params, charge_params


@pytest.fixture(scope="session")
def created_instance(config, instance_data, request):
    redis_cap = RedisCap(config, instance_data)
    # instance = Cluster(config, instance_data, http_client)
    accesser = Accesser(config)
    create_params, charge_params = get_create_params(instance_data)
    password = set_password("1qaz2WSX")
    create_params["password"] = password
    # 默认创建按配置计费的资源
    space_id, error = create_step(redis_cap, create_params, None)
    # 查询资源域名
    cluster_detail, error = query_detail_step(redis_cap, space_id)
    assert cluster_detail["cacheInstanceStatus"] == "running"

    # domain = cluster_detail["connectionDomain"]
    # ping资源域名，验证正确解析
    # ping_domain_step(accesser, space_id)

    def teardown():
        print
        info_logger.info("[TEARDOWN] Delete the instance {0}".format(space_id))
        delete_step(redis_cap, space_id)
        time.sleep(15)

    request.addfinalizer(teardown)
    return space_id, redis_cap, password, accesser


@pytest.fixture(scope="session")
def created_cluster(config, instance_data, request):
    redis_cap = RedisCap(config, instance_data)
    # instance = Cluster(config, instance_data, http_client)
    accesser = Accesser(config)
    create_params, charge_params = get_create_params(instance_data)
    password = set_password("1qaz2WSX")
    create_params["password"] = password
    create_params["cacheInstanceClass"] = instance_data["cache_cluster_class"]
    # 默认创建按配置计费的资源
    space_id, error = create_step(redis_cap, create_params, None)
    # 查询资源域名
    cluster_detail, error = query_detail_step(redis_cap, space_id)
    assert cluster_detail["cacheInstanceStatus"] == "running"

    # domain = cluster_detail["connectionDomain"]
    # ping资源域名，验证正确解析
    # ping_domain_step(accesser, space_id)

    def teardown():
        print
        info_logger.info("[TEARDOWN] Delete the instance {0}".format(space_id))
        delete_step(redis_cap, space_id)
        time.sleep(15)

    request.addfinalizer(teardown)
    return space_id, redis_cap, password, accesser


@pytest.fixture(scope="session")
def http_client(config):
    http_cli = HttpClient(config["web_host"], config["md5_pin"], config["auth_token"], "v3.0", config["tenant_id"], config["jcs_docker_host"], config["pin"])
    return http_cli
#
#
# @pytest.fixture(scope="session")
# def docker_client(config):
#     docker_cli = Container(config)
#     return docker_cli
#
#
# @pytest.fixture(scope="session")
# def sql_client(config):
#     sql_cli = SQLClient(config["mysql_host"], config["mysql_port"], config["mysql_user"], config["mysql_passwd"], config["mysql_db"])
#     return sql_cli


@pytest.fixture(scope="session", autouse=True)
def logger():
    info_logger = logging.getLogger()
    info_logger.setLevel(logging.INFO)

    formatter_debug = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    formatter_info = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

    info_log_name = './jmiss_redis28_test_log.INFO'
    info_file_handler = TimedRotatingFileHandler(info_log_name, 'midnight', 1, 31)
    info_file_handler.suffix = "%Y-%m-%d.log"
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter_debug)

    info_stdout_handler = logging.StreamHandler(sys.stdout)
    info_stdout_handler.setLevel(logging.INFO)
    info_stdout_handler.setFormatter(formatter_info)

    info_logger.addHandler(info_file_handler)
    info_logger.addHandler(info_stdout_handler)
