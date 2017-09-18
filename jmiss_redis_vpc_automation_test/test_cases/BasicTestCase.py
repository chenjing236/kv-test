# coding:utf-8

import pytest
from utils.HttpClient import *
from utils.SQLClient import *
from steps.ClusterOperation import *
from steps.ContainerOperation import *
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

info_logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def http_client(config):
    http_client = HttpClient(config["host"], config["pin"], config["auth_token"], config["version"],
                             config["tenant_id"], config["nova_docker_host"], config["nova_token_host"], config["user"])
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
    print "\n"
    info_logger.info("[SETUP] Create an instance including a master container and a slave container")
    instance = Cluster(config, instance_data, http_client)
    space_id, operation_id, password = create_instance_step(instance)
    info_logger.info("[INFO] The instance {0} is created, its password is {1}".format(space_id, password))
    # 查看创建操作结果，验证创建成功
    info_logger.info("[INFO] Get creation result of the instance {0}".format(space_id))
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, "[INFO] Get the right operation result, create instance successfully"

    def teardown():
        print "\n"
        info_logger.info("[TEARDOWN] Delete the instance {0}".format(space_id))
        instance.delete_instance(space_id)
        time.sleep(15)

    request.addfinalizer(teardown)
    return space_id, instance, password
