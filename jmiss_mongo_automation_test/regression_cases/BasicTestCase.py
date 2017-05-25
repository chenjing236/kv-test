# coding:utf-8

import pytest
import logging

info_logger = logging.getLogger(__name__)

# setup创建mongo实例，teardown删除mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance():
    #TODO，创建VPC和VPC下的子网
    info_logger.info("[PRE-CONDITION] ")

