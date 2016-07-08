import pytest
#import json
from utils.SQLClient import SQLClient
from utils.WebClient import *
from utils.JCacheUtils import *
from utils.DockerClient import *
from utils.Retry import *

def pytest_addoption(parser):
    parser.addoption("--config_file", action="store", default="conf.json",
                     help="test config file path")


@pytest.fixture(scope="session")
def config(request):
    #file_path = request.config.getoption("C:\Users\guoli5\git\JCacheTest\automation_test")
    file_path = "C:/Users/guoli5/git/JCacheTest/automation_test/conf.json"
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj


@pytest.fixture(scope="class")
def sql_client(config):
    sql_c = SQLClient(config['mysql_host'], config["mysql_port"], config["mysql_user"],
                      config["mysql_passwd"],
                      config["mysql_db"])
    return sql_c

@pytest.fixture(scope="class")
def web_client(config):
    wc = WebClient(config["host"], config["pin"], config["auth_token"])
    return wc

@pytest.fixture(scope="class")
def docker_client(config):
    docker_c = DockerClient(config)
    return docker_c

@pytest.fixture(scope="class")
def retry(config):
    retry_method = Retry(config)
    return retry_method

@pytest.fixture(scope="class")
def created_cluster(sql_client, web_client, request):
    ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 1, 1)
    space_id, space_info = CreateCluster(web_client, ca, sql_client)

    def teardown():
        DeleteCluster(web_client, space_id, sql_client)

    request.addfinalizer(teardown)
    return space_id, space_info
