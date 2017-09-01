# coding:utf-8

from utils.RedisClient import *
from business_function.Cluster import *
from business_function.Container import *

import json
import time
import logging

logger_info = logging.getLogger(__name__)


# 创建一个缓存云实例，返回缓存云实例的space_id
def create_instance_step(instance):
    res_data, password = instance.create_instance()
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to create an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of creating an instance is incorrect")
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    operation_id = attach["operationId"]
    return space_id, operation_id, password


# 获取创建后的缓存云实例的信息
def get_detail_info_of_instance_step(instance, space_id):
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    return attach


def get_operation_result_step(instance, space_id, operation_id):
    # 获取操作结果，判断对资源的操作是否成功
    code = 1
    count = 1
    retry_times = instance.conf_obj["retry_getting_info_times"]
    wait_time = instance.conf_obj["wait_time"]
    while code == 1 and count < retry_times:
        res_data = instance.get_operation_result(space_id, operation_id)
        code = res_data["code"]
        msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
        assert code == 0, "[ERROR] It is failed to get operation result, error message is {0}".format(msg)
        attach = res_data["attach"]
        if attach is None or attach is "":
            logger_info.error("[ERROR] Response of getting operation result is incorrect")
            assert False, "[ERROR] Response of getting operation result is incorrect"
        logger_info.info("[INFO] Response of getting operation result is [{0}]".format(attach))
        code = attach["code"]
        count += 1
        time.sleep(wait_time)
    if count >= retry_times:
        assert False, "[ERROR] The operation of instance is failed"
    if code != 0:
        assert False, "[ERROR] The operation of instance is failed, error_code = {0}".format(code)
    return True


# # 获取创建后的缓存云实例的状态
# def get_status_of_instance_step(instance, space_id, retry_times, wait_time):
#     res_data = instance.get_instance_info(space_id)
#     code = res_data["code"]
#     msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
#     assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
#     attach = res_data["attach"]
#     if attach is None or attach is "":
#         logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
#         assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
#     status = attach["status"]
#     capacity = int(attach["capacity"])
#     count = 1
#     while status != 100 and count < retry_times:
#         res_data = instance.get_instance_info(space_id)
#         if res_data is None or res_data is "":
#             logger_info.error("[ERROR] It is failed to get topology from detail information of the instance %s.", space_id)
#             assert False, "[ERROR] It is failed to get topology from detail information of the instance {0}.".format(space_id)
#         attach = res_data["attach"]
#         status = attach["status"]
#         logger_info.info("[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status))
#         count += 1
#         time.sleep(wait_time)
#     return status, capacity


#
def get_topology_of_instance_step(instance, space_id):
    res_data = instance.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Cannot get detail information of the instance {0}".format(space_id)
    masterIp, masterPort, slaveIp, slavePort = instance.get_topology_of_instance(res_data)
    return masterIp, masterPort, slaveIp, slavePort


def get_topology_of_cluster_step(instance, space_id):
    res_data = instance.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Cannot get detail information of the instance {0}".format(space_id)
    shards = instance.get_topology_of_cluster(res_data, space_id)
    return shards


def get_topology_of_instance_from_cfs_step(cfs_client, space_id):
    res_data = cfs_client.get_meta(space_id)
    print res_data
    if res_data is None or res_data is "":
        assert False, "[ERROR] It is failed to get topology from CFS."
    currentTopology = res_data["currentTopology"]
    if currentTopology is None or currentTopology is "":
        assert False, "[ERROR] The information of topology is incorrect from CFS."
    master_host_ip, master_docker_id, slave_host_ip, slave_docker_id = cfs_client.get_topology_from_cfs(currentTopology)
    return master_host_ip, master_docker_id, slave_host_ip, slave_docker_id


def get_topology_of_cluster_from_cfs_step(cfs_client, space_id):
    res_data = cfs_client.get_meta(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] It is failed to get topology from CFS."
    currentTopology = res_data["currentTopology"]
    if currentTopology is None or currentTopology is "":
        assert False, "[ERROR] The information of topology is incorrect from CFS."
    shards = cfs_client.get_topology_of_cluster_from_cfs(currentTopology)
    return shards


def delete_instance_step(instance, space_id):
    res_data = instance.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
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
    assert value_slave == value, "[ERROR] Cannot get the key just set"
    return True, key, value


def resize_instance_step(instance, space_id, flavor_id):
    # 执行resize扩容操作
    res_data = instance.resize_instance(space_id, flavor_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to resize an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of resizing an instance is incorrect")
        assert False, "[ERROR] Response of resizing an instance is incorrect"
    operation_id = attach["operationId"]
    # 获取操作结果，判断扩容是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, "[INFO] Get the right operation result, resize instance failed"
    # 获取capacity
    info_new = instance.get_instance_info(space_id)
    attach_new = info_new["attach"]
    status = attach_new["status"]
    flavor_id_new = attach_new["flavorId"]
    return status, flavor_id_new


def set_key_from_ap_step(ap_host, ap_port, password, key, value):
    redis_client = RedisClient(ap_host, ap_port, password)
    key_from_ap, value_from_ap = redis_client.set_value_from_ap_by_key(ap_host, ap_port, password, key, value)
    return key_from_ap, value_from_ap


def get_key_from_ap_step(ap_host, ap_port, password, key):
    redis_client = RedisClient(ap_host, ap_port, password)
    value_from_ap = redis_client.get_value_from_ap_by_key(ap_host, ap_port, password, key)
    return value_from_ap


# 执行failover操作
def run_failover_container_step(space_id, container_id, container, cfs_client, failover_type):
    # 查询CFS的redis，查看epoch的值
    if cfs_client is None:
        assert False, "[ERROR] CFS client is not initialed"
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, "[ERROR] Cannot get topology information from cfs"
    epoch_origin = res_data["epoch"]
    # stop指定的container
    container.delete_nova_docker(container_id)
    logger_info.info("[INFO] Success to stop container [{0}]".format(container_id))
    # 查询CFS的redis，查看epoch的值是否有变化
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, "[ERROR] Cannot get topology information from cfs"
    epoch_new = res_data["epoch"]
    count = 0
    retry_times = container.conf_obj["retry_getting_topology_from_cfs"]
    wait_time = container.conf_obj["wait_time"]
    # failover_type=2: master failover
    # failover_type=1: slave failover
    while epoch_new != epoch_origin + failover_type and count < retry_times:
        res_data = cfs_client.get_meta(space_id)
        if res_data is None:
            assert False, "[ERROR] Cannot get topology information from cfs"
        epoch_new = res_data["epoch"]
        count += 1
        time.sleep(wait_time)
    if count == retry_times:
        return False
    return True


def run_failover_container_of_cluster_step(cfs_client, container, space_id, failover_type, masterIp, masterPort, retry_times, wait_time):
    is_failover = run_failover_container_step(space_id, masterIp, masterPort, container, cfs_client, retry_times, wait_time, failover_type)
    assert is_failover is True, "[ERROR] It is failed to run master failover"
    logger_info.info("[INFO] It is successful to run master failover")
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, "[ERROR] It is failed to get topology after running master failover."
    currentTopology = res_data["currentTopology"]
    master_ip_new, master_port_new, slave_ip_new, slave_port_new = cfs_client.get_topology_from_cfs(currentTopology)
    return is_failover, master_ip_new, master_port_new, slave_ip_new, slave_port_new


def run_rebuild_upgrade_step(instance, space_id):
    res_data = instance.rebuild_upgrade_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to upgrade an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of upgrading an instance is incorrect")
        assert False, "[ERROR] Response of upgrading an instance is incorrect"
    operation_id_upgrade = attach["operationId"]
    # 获取操作结果，判断repair是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id_upgrade)
    assert is_success is True, "[INFO] Get the right operation result, rebuild-upgrade instance failed"
    logger_info.info("[INFO] Run rebuild upgrade successfully, The space_id of upgrade instance is {0}".format(space_id))
    return True


def run_rebuild_repair_step(instance, space_id, container, cfs_client):
    # 获取原有epoch
    masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
    # stop master and slave container
    container.delete_nova_docker(masterDocker)
    container.delete_nova_docker(slaveDocker)
    # check space status = 101
    detail_info = get_detail_info_of_instance_step(instance, space_id)
    status = detail_info["status"]
    retry_times = instance.conf_obj["retry_getting_topology_from_cfs"]
    wait_time = instance.conf_obj["wait_time"]
    count = 1
    while status != 101 and count < retry_times:
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        status = detail_info["status"]
        logger_info.info("[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status))
        count += 1
        time.sleep(wait_time)
    # run rebuild repair
    logger_info.info("[INFO] Start to run rebuild repair")
    res_data = instance.rebuild_repair_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    operation_id_repair = res_data["attach"]["operationId"]
    assert code == 0, "[ERROR] It is failed to rebuild repair instance {0}, error message is {1}".format(space_id, msg)
    # 获取操作结果，判断repair是否成功
    get_operation_result_step(instance, space_id, operation_id_repair)
    logger_info.info("[INFO] Run rebuild repair successfully")
    return True


def run_rebuild_clone_step(instance, space_id):
    res_data = instance.rebuild_clone_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to clone an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of cloning an instance is incorrect")
        assert False, "[ERROR] Response of cloning an instance is incorrect"
    space_id = attach["spaceId"]
    operation_id_clone = attach["operationId"]
    # 获取操作结果，判断repair是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id_clone)
    assert is_success is True, "[INFO] Get the right operation result, rebuild-upgrade instance failed"
    logger_info.info("[INFO] Run rebuild clone successfully, The space_id of clone instance is {0}".format(space_id))
    return space_id


def reset_password_step(instance, space_id, password):
    res_data = instance.reset_password(space_id, password)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of reset_password is incorrect for the instance {0}".format(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to reset password, error message is {0}".format(msg)


def get_clusters_step(instance):
    res_data = instance.get_clusters()
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_clusters is incorrect"
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get clusters, error message is {0}".format(msg)
    return res_data["attach"]


def get_filter_clusters_step(instance, filterName="", filterSpaceType="", filterStatus="", sortName="", sortRule="",
                             pageSize="", pageNum=""):
    filters = "filterName={0}&filterSpaceType={1}&filterStatus={2}&sortName={3}&sortRule={4}&pageSize={5}&" \
              "pageNum={6}".format(filterName, filterSpaceType, filterStatus, sortName, sortRule, pageSize, pageNum)
    res_data = instance.get_filter_clusters(filters)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_clusters is incorrect"
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get clusters, error message is {0}".format(msg)
    return res_data["attach"]


def update_meta_step(instance, space_id, name, remarks):
    res_data = instance.update_meta(space_id, name, remarks)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of update_meta is incorrect for the instance {0}".format(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to update meta, error message is {0}".format(msg)


def get_realtime_info_step(instance, space_id):
    res_data = instance.get_realtime_info(space_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_realtime_info is incorrect for the instance {0}".format(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get realtime info, error message is {0}".format(msg)
    return res_data["attach"]


def get_resource_info_step(instance, space_id, period="15m", frequency="3m"):
    res_data = instance.get_resource_info(space_id, period, frequency)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of get_resource_info is incorrect for the instance {0}".format(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get resource info, error message is {0}".format(msg)
    return res_data["attach"]


def query_flavor_id_by_config_step(instance, cpu, memory, disk, max_connections, net):
    flavor = {"cpu": cpu, "memory": memory, "disk": disk, "max_connections": max_connections, "net": net}
    res_data = instance.query_flavor_id_by_config(flavor)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of query_flavor_id_by_config is incorrect for the flavor {0}".format(flavor)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to query flavorId by config, error message is {0}".format(msg)
    return res_data["attach"]


def query_config_by_flavor_id_step(instance, flavor_id):
    res_data = instance.query_config_by_flavor_id(flavor_id)
    if res_data is None or res_data is "":
        assert False, "[ERROR] Response of query_config_by_flavor_id is incorrect for the flavor [{0}]".format(flavor_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to query config by flavorId, error message is {0}".format(msg)
    return res_data["attach"]


def change_topology_json_to_list(shard_count, topology):
    shards = []
    for i in range(0, shard_count):
        if 'shards' not in topology or topology['shards'] is None or len(topology['shards']) == 0 or 'master' not in topology['shards'][i]:
            return None
        else:
            master = topology['shards'][i]['master']
            master_ip = master['ip']
            master_port = master['port']
        if 'slaves' not in master or master['slaves'] is None or len(master['slaves']) == 0:
            slave_ip = None
            slave_port = None
        else:
            slave = master['slaves'][0]
            slave_ip = slave['ip']
            slave_port = slave['port']
        shard = {"masterIp": master_ip, "masterPort": master_port, "slaveIp": slave_ip, "slavePort": slave_port}
        shards.append(shard)
    return shards
