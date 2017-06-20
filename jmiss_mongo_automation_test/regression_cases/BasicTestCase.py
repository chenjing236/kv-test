# -*- coding: utf-8 -*- 

import pytest
import logging
from steps.ClusterOperationSteps import *
from steps.FlavorOperationsSteps import *
from steps.ContainerOperationSteps import *

info_logger = logging.getLogger(__name__)

# setup创建mongo实例，teardown删除mongo实例
@pytest.fixture(scope="class")
def create_mongo_instance(request, config, instance_data, http_client):
    #TODO，创建VPC和VPC下的子网
    info_logger.info("[PRE-CONDITION] Create a VPC and subnet under the VPC")
    print "[PRE-CONDITION] Create a VPC and subnet under the VPC"
    info_logger.info("[STEP] Create a mongo instance")
    space_id = create_mongo_instance_step(config, instance_data, http_client)
    info_logger.info("[INFO] The mongo %s is being created", space_id)
    info_logger.info("[STEP] Get status of the mongo instance %s", space_id)
    status = get_status_of_instance_step(config, instance_data, http_client, space_id)
    info_logger.info("[INFO] The status of the mongo %s is %s", space_id, status)
    assert status == 100, "[ERROR] Instance {0} is unavailable".format(space_id)

    def teardown():
        print "\n[TEARDOWN] Delete the instance {0}".format(space_id)
        info_logger.info("[TEARDOWN] Delete the mongo instance %s", space_id)
        delete_instance_step(config, instance_data, http_client, space_id)

    request.addfinalizer(teardown)
    return space_id
