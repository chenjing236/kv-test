#!/usr/bin/python
# coding:utf-8
import pytest
import json
#import sys
#sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/utils")
#from HttpClient import *
#from RedisClient import *
#sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/business_function")
#from Cluster import *
#from Container import *
#from CFS import *
#sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/steps")
#from ClusterOperation import *

from utils.HttpClient import *
from utils.RedisClient import *
from utils.util import *
from business_function.Cluster import *
from business_function.Container import *
from business_function.CFS import *
from steps.ClusterOperation import *

def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="conf.json", help="test config file path")
    parser.addoption("--data", action="store", default="instance_data.json", help="data file path")

@pytest.fixture(scope="session", autouse=True)
def config(request):
    #file_path = request.config.getoption("config")
    #file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    file_path = cur_file_dir().replace("\\","/").replace("test_cases", "") + "config/conf.json"
    print "[INFO] Current path is {0}".format(file_path)
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj

@pytest.fixture(scope="session")
def instance_data(request):
    #file_path = request.config.getoption("--data")
    #file_path="C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/data/instance_data.json"
    file_path = cur_file_dir().replace("\\","/").replace("test_cases", "") + "data/instance_data.json"
    data = json.load(open(file_path, 'r'))
    return data

@pytest.fixture(scope="class")
def http_client(config):
    http_client = HttpClient(config["host"], config["pin"], config["auth_token"])
    return http_client

@pytest.fixture(scope="class")
def docker_client(config):
    docker_client = Container(config)
    return docker_client

@pytest.fixture(scope="class")
def created_instance(config, instance_data, http_client, request):
    print "\n[SETUP] Create an instance with a master container and a slave container"
    instance = Cluster(config, instance_data, http_client)
    space_id = create_instance_step(instance)
    status, capacity = get_status_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
    assert status == 100

    def teardown():
        print "\n[TEARDONW] Delete the instance {0}".format(space_id)
        instance.delete_instance(space_id)

    request.addfinalizer(teardown)
    return space_id, instance
