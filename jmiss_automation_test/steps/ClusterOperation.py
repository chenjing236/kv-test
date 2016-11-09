#!/usr/bin/python
# coding:utf-8
import sys
sys.path.append("C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/business_function")
from Cluster import *
from Container import *
import json
import time

#创建一个缓存云实例，返回缓存云实例的space_id
def create_instance_step(instance):
    res_data = instance.create_instance()
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to create an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    return space_id

def get_detail_info_of_instance_step(instance, space_id, retry_times, wait_time):
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    status = attach["status"]
    capacity = int(attach["capacity"])
    count = 1
    while status != 100 and count < retry_times:
        res_data = instance.get_instance_info(space_id)
        if res_data is None or res_data is "":
            assert False, "[ERROR] It is failed to get topology from detail information of the instance {0}.".format(space_id)
        attach = res_data["attach"]
        status = attach["status"]
        attach = res_data["attach"]
        print "[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status)
        count += 1
        time.sleep(wait_time)
    return status, capacity

def get_topology_of_instance_step(instance, space_id):
    res_data = instance.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Cannot get detail information of the instanceh {0}".format(space_id)
    masterIp, masterPort, slaveIp, slavePort = instance.get_topology_of_instance(res_data, space_id)
    return masterIp, masterPort, slaveIp, slavePort

def get_topology_of_instance_from_cfs_step(cfs_client, space_id):
    res_data = cfs_client.get_meta(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] It is failed to get topology from CFS."
    currentTopology = res_data["currentTopology"]
    if currentTopology is None or currentTopology is "":
        assert False, "[ERROR] The information of topology is incorrect from CFS."
    master_ip, master_port, slaveIp, slavePort = cfs_client.get_topology_from_cfs(currentTopology)
    return master_ip, master_port, slaveIp, slavePort

def get_container_memory_size(container, masterIp, masterPort, slaveIp, slavePort):
    master_memory_size = container.get_memory_size_of_container(masterIp, masterPort)
    slave_memory_size = container.get_memory_size_of_container(slaveIp, slavePort)
    return master_memory_size, slave_memory_size

def delete_instance(instance, space_id):
    res_data = instance.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to delete the instance {0}, error message is {1}".format(space_id, msg)