# encoding:utf-8

import pytest
import logging
from business_function.Cluster import *
from steps.ClusterOperationSteps import *

info_logger = logging.getLogger(__name__)

# setup创建mongo实例，teardown删除mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance(config, instance_data, http_client):
    #TODO，创建VPC和VPC下的子网
    info_logger.info("[PRE-CONDITION] Create a VPC and subnet under the VPC")
    print "[PRE-CONDITION] Create a VPC and subnet under the VPC"
    mongo_instance_info = Cluster(config, instance_data, http_client)
    space_id = create_mongo_instance_step(mongo_instance_info)
    print "[MONGO] space_id is {0}".format(space_id)
