# coding:utf-8

import pytest
import logging

info_logger = logging.getLogger(__name__)

# setup创建mongo实例，teardown删除mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance():
    #TODO，创建VPC和VPC下的子网
    info_logger.info("[PRE-CONDITION] Create a VPC and subnet under the VPC")
    print "[PRE-CONDITION] Create a VPC and subnet under the VPC"
    #mongo_instance = Cluster(config, instance_data, http_client)
    #space_id = create_mongo_instance_step(mongo_instance)
    #print "[MONGO] space_id is {0}".format(space_id)
