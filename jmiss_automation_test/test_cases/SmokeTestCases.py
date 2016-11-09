#!/usr/bin/python
# coding:utf-8
import pytest
from BasicTestCase import *
import sys
sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/steps")
from ClusterOperation import *

class TestSmokeCases:

    @pytest.mark.smoke
    def test_create_an_instance(self, config, instance_data, http_client):
        print "\n[SCENARIO] Create an instance including a master container and a slave container"
        instance = Cluster(config, instance_data, http_client)
        #创建缓存云实例
        print "[STEP1] Create an instance including a master container and a slave container"
        space_id = create_instance_step(instance)
        print "[INFO] The instance {0} is created".format(space_id)
        #查看缓存云实例详细信息
        print "[STEP2] Get detailed information of the instance {0}".format(space_id)
        status, capacity = get_detail_info_of_instance_step(instance, space_id, int(config["retry_getting_info_times"]), int(config["wait_time"]))
        print "[INFO] Status of the instance {0} is {1}".format(space_id, status)
        #验证缓存云实例状态，status=100创建成功
        assert status == 100
        #查看缓存云实例详情，获取拓扑结构
        print "[STEP3] Get topology information of instance"
        masterIp, masterPort, slaveIp, slavePort = get_topology_of_instance_step(instance, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp, masterPort)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp, slavePort)
        #获取CFS的拓扑结构
        print "[STEP4] Get topology information of instance from CFS"
        cfs_client = CFS(config)
        masterIp_cfs, masterPort_cfs, slaveIp_cfs, slavePort_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        print "[INFO] Information of master container is {0}:{1}".format(masterIp_cfs, masterPort_cfs)
        print "[INFO] Information of slave container is {0}:{1}".format(slaveIp_cfs, slavePort_cfs)
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterPort == masterPort_cfs, "[ERROR] Port of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slavePort == slavePort_cfs, "[ERROR] Port of slave container is inconsistent"
        #获取container的大小，验证container的大小
        container = Container(config)
        master_memory_size, slave_memory_size = get_container_memory_size(container, masterIp, masterPort, slaveIp, slavePort)
        print "[INFO] Memory size of master container is {0}".format(master_memory_size)
        print "[INFO] Memory size of slave container is {0}".format(slave_memory_size)
        assert master_memory_size == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert slave_memory_size == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        #删除缓存云实例
        print "[STEP5] Delete the instance {0}".format(space_id)
        delete_instance(instance, space_id)

    def test_access_ap(self):
        print "\n[SCENARIO] It is successfull to access AP and to set/get key"
        #


