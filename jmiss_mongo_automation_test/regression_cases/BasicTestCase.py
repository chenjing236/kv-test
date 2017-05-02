# coding:utf-8

import pytest
import logging

info_logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def http_client(config):
    http_client = HttpClient(config["host"], config["pin"], config["auth_token"], config["version"])
    return http_client

def create_vpc():
    info_logger.info("[CONDITION] Create a VPC")
    return vpc_id

def create_subnet(vpc_id):
    info_logger.info("[CONDITION] Create a subnet under the VPC {0}".format(vpc_id))
    return subnet_id