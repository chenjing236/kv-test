# coding:utf-8
import pytest
from utils.HttpClient import *
from utils.SQLClient import *
from utils.RedisClient import *
from utils.util import *
from business_function.Cluster import *
from business_function.Container import *
from business_function.CFS import *
from steps.ClusterOperation import *
import logging

info_logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def http_client(config):
    http_client = HttpClient(config["host"], config["pin"], config["auth_token"])
    return http_client

@pytest.fixture(scope="class")
def docker_client(config):
    docker_client = Container(config)
    return docker_client

@pytest.fixture(scope="class")
def sql_client(config):
    sql_client = SQLClient(config["mysql_host"], config["mysql_port"],
                           config["mysql_user"], config["mysql_passwd"],
                           config["mysql_db"])
    return sql_client

@pytest.fixture(scope="class")
def created_instance(config, instance_data, http_client, request):
    print "\n[SETUP] Create an instance with a master container and a slave container"
    info_logger.info("[SETUP] Create an instance with a master container and a slave container")
    instance = Cluster(config, instance_data, http_client)
    space_id = create_instance_step(instance)
    status, capacity = get_status_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
    assert status == 100, "[ERROR] Instance {0} is inavialble".format(space_id)

    def teardown():
        print "\n[TEARDOWN] Delete the instance {0}".format(space_id)
        info_logger.info("[TEARDOWN] Delete the instance %s", space_id)
        instance.delete_instance(space_id)

    request.addfinalizer(teardown)
    return space_id, instance
