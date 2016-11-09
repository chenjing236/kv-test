#!/usr/bin/python
# coding:utf-8
import pytest
import json
import sys
sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/utils")
from HttpClient import *
sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/business_function")
from Cluster import *
from Container import *
from CFS import *

@pytest.fixture(scope="session")
def config(request):
    #file_path = request.config.getoption("config_file")
    file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj

@pytest.fixture(scope="session")
def instance_data(request):
    #file_path = request.config.getoption("instance_data")
    file_path="C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/data/instance_data.json"
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
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.create_instance()
    attach = res_data["attach"]
    space_id = attach["spaceId"]

    def teardown():
        print "[INFO] delete instance {0}".format(space_id)
        instance.delete_instance(space_id)

    request.addfinalizer(teardown)
    return space_id, res_data