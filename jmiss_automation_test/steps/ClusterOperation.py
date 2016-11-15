# coding:utf-8

from utils.DockerClient import *
from utils.RedisClient import *
from business_function.Cluster import *
from business_function.Container import *

import json
import time
import logging

logger_info = logging.getLogger(__name__)

#创建一个缓存云实例，返回缓存云实例的space_id
def create_instance_step(instance):
    res_data = instance.create_instance()
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to create an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of creating an instance is incorrect")
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    return space_id

#获取创建后的缓存云实例的信息
def get_detail_info_of_instance_step(instance, space_id):
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    return attach

#获取创建后的缓存云实例的状态
def get_status_of_instance_step(instance, space_id, retry_times, wait_time):
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    status = attach["status"]
    capacity = int(attach["capacity"])
    count = 1
    while status != 100 and count < retry_times:
        res_data = instance.get_instance_info(space_id)
        if res_data is None or res_data is "":
            logger_info.error("[ERROR] It is failed to get topology from detail information of the instance %s.", space_id)
            assert False, "[ERROR] It is failed to get topology from detail information of the instance {0}.".format(space_id)
        attach = res_data["attach"]
        status = attach["status"]
        attach = res_data["attach"]
        print "[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status)
        count += 1
        time.sleep(wait_time)
    return status, capacity

#
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

def set_acl_step(instance, space_id, ips):
    res_data = instance.set_acl(space_id, ips)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of setting acl is incorrect for the instance {0}".format(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to set acl, error message is {0}".format(msg)

def get_acl_step(instance, space_id):
    res_data = instance.get_acl(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to set acl, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        assert False, "[ERROR] Cannot get acl for the instance {0}".format(space_id)
    return attach["ips"]

def delete_instance_step(instance, space_id):
    res_data = instance.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to delete the instance {0}, error message is {1}".format(space_id, msg)

def access_ap_step(ap_host, ap_port, password):
    redis_client = RedisClient(ap_host, ap_port, password)
    return redis_client.check_ap_access(ap_host, ap_port, password)

def access_container_step(masterIp, masterPort, slaveIp, slavePort):
     redis_client = RedisClient(masterIp, masterPort, None)
     key = "test_key_resize"
     value = "test_key_before_resize"
     redis_client.set_key_value_for_master(masterIp, masterPort, key, value)
     value_slave = redis_client.get_value_from_slave(slaveIp, slavePort, key)
     assert value_slave == value, "[ERROR] Cannot get the key just setted"
     return True, key, value

def resize_instance_step(instance, cfs_client , space_id, zoneId, capacity, retry_times, wait_time):
    #获取原有epoch
    res_data_cfs_origin = cfs_client.get_meta(space_id)
    epoch_origin = res_data_cfs_origin["epoch"]
    #执行resize扩容操作
    res_data = instance.resize_instance(space_id, zoneId, capacity)
    if res_data is None or res_data is "":
        assert False,"[ERROR] Response of resizing the instanche {0} is incorrect".format(space_id)
    #执行扩容后的CFS拓扑结构中的epoch
    res_data_cfs = cfs_client.get_meta(space_id)
    epoch = res_data_cfs["epoch"]
    count = 1
    while epoch == epoch_origin and count < retry_times:
        res_data_cfs = cfs_client.get_meta(space_id)
        epoch = res_data_cfs["epoch"]
        count +=1
        time.sleep(wait_time)
    if count >= retry_times:
        assert False, "[ERROR] It is failed to resize instance"
    #获取capacity
    info_new = instance.get_instance_info(space_id)
    attach_new = info_new["attach"]
    status = attach_new["status"]
    capacity_new = attach_new["capacity"]
    return status, capacity_new

def get_key_from_ap_step(ap_host, ap_port, password, key):
    redis_client = RedisClient(ap_host, ap_port, password)
    value_from_ap = redis_client.get_value_from_ap_by_key(ap_host, ap_port, password, key)
    return value_from_ap

#执行failover操作
def run_failover_container(space_id, containerIp, containerPort, docker_client, cfs_client, retry_times, wait_time):
    #查询CFS的redis，查看epoch的值
    if cfs_client == None:
        assert False, "[ERROR] CFS client is not initialed"
    res_data = cfs_client.get_meta(space_id)
    if res_data == None:
        assert False, "[ERROR] Cannot get topology information from cfs"
    epoch_origin = res_data["epoch"]
    #stop指定的container
    docker_client.stop_container(containerIp, containerPort)
    #查询CFS的redis，查看epoch的值是否有变化
    res_data = cfs_client.get_meta(space_id)
    if res_data == None:
        assert False, "[ERROR] Cannot get topology information from cfs"
    epoch_new = res_data["epoch"]

    count = 0;
    while epoch_new == epoch_origin and count <  retry_times:
        res_data = cfs_client.get_meta(space_id)
        if res_data == None:
            assert False, "[ERROR] Cannot get topology information from cfs"
        epoch_new = res_data["epoch"]
        count += 1
        time.sleep(wait_time)
    if count == retry_times:
        return False
    return True

def run_failover_container_step(instance, cfs_client, container, space_id, masterIp, masterPort, retry_times, wait_time):
    is_failover = run_failover_container(space_id, masterIp, masterPort, container, cfs_client, retry_times, wait_time)
    assert is_failover == True,"[ERROR] It is failed to run master failover"
    print "[INFO] It is succesfull to run master failover"
    res_data = cfs_client.get_meta(space_id)
    if res_data == None:
        assert False, "[ERROR] It is failed to get topology after running master failover."
    currentTopology = res_data["currentTopology"]
    master_ip_new, master_port_new, slaveIp_new, slavePort_new = cfs_client.get_topology_from_cfs(currentTopology)
    return is_failover, master_ip_new, master_port_new, slaveIp_new, slavePort_new

