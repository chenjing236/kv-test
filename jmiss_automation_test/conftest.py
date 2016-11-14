import pytest
import sys
import json
from utils.util import *

def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="conf.json", help="test config file path")
    parser.addoption("--data", action="store", default="instance_data.json", help="data file path")

@pytest.fixture(scope="session", autouse=True)
def config(request):
    file_path = request.config.getoption("config")
    #file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    file_path = cur_file_dir().replace("\\","/").replace("test_cases", "") + "config/conf.json"
    conf_obj = json.load(open(file_path, 'r'))
    return conf_obj

@pytest.fixture(scope="session")
def instance_data(request):
    #file_path = request.config.getoption("--data")
    #file_path="C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/data/instance_data.json"
    file_path = cur_file_dir().replace("\\","/").replace("test_cases", "") + "data/instance_data.json"
    data = json.load(open(file_path, 'r'))
    return data