# coding:utf-8
# import time
from business_function.Cluster import *
from ContainerOperation import *
from AccessOperation import *
from business_function.CFS import *
from business_function.Scaler import *
from business_function.RedisCap import *
import logging
info_logger = logging.getLogger(__name__)


# check_keys: 用于扩容时，验证扩容过程中正确读取分布在不同slots上的数据
def get_operation_result_step(instance, space_id, operation_id, check_keys=False, accesser=None, password=None):
    # 获取操作结果，判断对资源的操作是否成功
    info_logger.info("[STEP] Get creation result of the instance {0}".format(space_id))
    code = 1
    count = 1
    retry_times = instance.conf_obj["retry_getting_info_times"]
    wait_time = instance.conf_obj["wait_time"]
    while code == 1 and count < retry_times:
        res_data = instance.get_operation_result(space_id, operation_id)
        code = res_data["code"]
        msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
        assert code == 0, info_logger.error("It is failed to get operation result, error message is {0}".format(msg))
        attach = res_data["attach"]
        if attach is None or attach is "":
            info_logger.error("Response of getting operation result is incorrect")
            assert False, info_logger.error("Response of getting operation result is incorrect")
        info_logger.info("Response of [{0} times] getting operation result is [{1}]".format(count, attach["message"]))
        code = attach["code"]
        count += 1
        # 扩容过程中读取分布在不同slots上的数据
        if check_keys is True:
            query_test_keys(accesser, space_id, password)
        time.sleep(wait_time)
    if count >= retry_times:
        assert False, info_logger.error("The operation of instance is failed")
    if code != 0:
        assert False, info_logger.error("The operation of instance is failed, error_code = {0}".format(code))
    # info_logger.info("Get the right operation result, create instance successfully")
    return True


def set_system_acl_step(instance, space_id, enable):
    res_data = instance.set_system_acl(space_id, enable)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of setting system acl is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to set system acl, error message is {0}".format(msg))


# 通过查询详情接口获取资源proxy列表
def get_proxy_list_of_instance_step(instance, space_id):
    info_logger.info("[STEP] Get proxy list of instance")
    res_data = instance.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Cannot get detail information of the instance {0}".format(space_id))
    proxy_list = instance.get_proxy_list_of_instance(res_data)
    for i in range(0, len(proxy_list)):
        info_logger.info("Information of proxy_{0} is [{1}: {2}, {3}, {4}]".format(i, proxy_list[i]["proxyId"], proxy_list[i]["hostIp"], proxy_list[i]["dockerId"], proxy_list[i]["overlayIp"]))
    return proxy_list


# 通过查询详情接口获取主从资源拓扑结构
def get_topology_of_instance_step(instance, space_id):
    info_logger.info("[STEP] Get topology information of instance")
    res_data = instance.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Cannot get detail information of the instance {0}".format(space_id))
    masterIp, master_docker_id, slaveIp, slave_docker_id = instance.get_topology_of_instance(res_data)
    info_logger.info("Information of master container is {0}: [{1}]".format(masterIp, master_docker_id))
    info_logger.info("Information of slave container is {0}: [{1}]".format(slaveIp, slave_docker_id))
    return masterIp, master_docker_id, slaveIp, slave_docker_id


# 通过查询详情接口获取集群资源拓扑结构
def get_topology_of_cluster_step(cluster, space_id):
    info_logger.info("[STEP] Get topology information of cluster {0}".format(space_id))
    res_data = cluster.get_instance_info(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Cannot get detail information of the instance {0}".format(space_id))
    shards = cluster.get_topology_of_cluster(res_data)
    shard_count = len(shards)
    info_logger.info("The count of shards of cluster is {0}".format(shard_count))
    for i in range(0, shard_count):
        info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
    return shards


# 通过查询CFS接口获取主从资源拓扑结构
def get_topology_of_instance_from_cfs_step(cfs_client, space_id):
    info_logger.info("[STEP] Get topology information of instance from CFS")
    res_data = cfs_client.get_meta(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("It is failed to get topology from CFS.")
    currentTopology = res_data["currentTopology"]
    if currentTopology is None or currentTopology is "":
        assert False, info_logger.error("The information of topology is incorrect from CFS.")
    master_ip, master_docker_id, slave_ip, slave_docker_id = cfs_client.get_topology_from_cfs(currentTopology)
    info_logger.info("Information of master container from cfs is {0}: [{1}]".format(master_ip, master_docker_id))
    info_logger.info("Information of slave container from cfs is {0}: [{1}]".format(slave_ip, slave_docker_id))
    return master_ip, master_docker_id, slave_ip, slave_docker_id


# 通过查询CFS接口获取集群资源拓扑结构
def get_topology_of_cluster_from_cfs_step(cfs_client, space_id):
    info_logger.info("[STEP] Get topology information of cluster from CFS")
    res_data = cfs_client.get_meta(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("It is failed to get topology from CFS.")
    currentTopology = res_data["currentTopology"]
    if currentTopology is None or currentTopology is "":
        assert False, info_logger.error("The information of topology is incorrect from CFS.")
    shards = cfs_client.get_topology_of_cluster_from_cfs(currentTopology)
    shard_count = len(shards)
    for i in range(0, shard_count):
        info_logger.info("Information of shard_{0} container is {1}".format(i + 1, shards[i]))
    return shards


# 验证数据库中topology version与ap内存中一致
def check_topology_verison_of_ap_step(container, sql_client, space_id):
    info_logger.info("[STEP] Check topology version of proxy and mysql")
    sql_str = "select current_topology from topology where space_id='{0}'".format(space_id)
    result = sql_client.exec_query_one(sql_str)
    topology = json.loads(result[0])
    topology_version = topology["version"]
    sql_str = "select host_ip, docker_id from ap where space_id='{0}' order by id desc".format(space_id)
    result = sql_client.exec_query_one(sql_str)
    ap_host_ip = result[0]
    ap_docker_id = result[1]
    ap_version = ping_ap_version_step(container, ap_host_ip, ap_docker_id, space_id)
    assert ap_version == topology_version, \
        info_logger.error("Topology version of ap and mysql is not same! "
                            "Ap[{0}] version is [{1}], mysql version is [{2}]".format(ap_docker_id, ap_version, topology_version))
    info_logger.info("Check topology version of proxy and mysql successfully!")
    return True


# 对redis资源执行failover操作，包括主从版和集群版分片
def run_failover_container_step(space_id, container_id, container, cfs_client, failover_type):
    info_logger.info("[STEP] Run failover for redis container")
    # 查询CFS的redis，查看epoch的值
    if cfs_client is None:
        assert False, info_logger.error("CFS client is not initialed")
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, info_logger.error("Cannot get topology information from cfs")
    epoch_origin = res_data["epoch"]
    # stop指定的container
    container.stop_jcs_docker(container_id)
    info_logger.info("Success to stop container [{0}]".format(container_id))
    # 查询CFS的redis，查看epoch的值是否有变化
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, info_logger.error("Cannot get topology information from cfs")
    epoch_new = res_data["epoch"]
    count = 0
    retry_times = container.conf_obj["retry_failover_wait_times"]
    wait_time = container.conf_obj["wait_time"]
    # failover_type=2: master failover
    # failover_type=1: slave failover
    while epoch_new != epoch_origin + failover_type and count < retry_times:
        res_data = cfs_client.get_meta(space_id)
        if res_data is None:
            assert False, info_logger.error("Cannot get topology information from cfs")
        epoch_new = res_data["epoch"]
        count += 1
        time.sleep(wait_time)
    if count == retry_times:
        return False
    info_logger.info("It is successful to run redis failover")
    return True


# 通过web get_cluster_info接口查询当前主CFS
def get_master_server_step(instance, server_name):
    info_logger.info("[STEP] To get master {0}.".format(server_name))
    res_data = instance.op_get_cluster_info()
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of op_get_cluster_info is incorrect".format())
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get cluster op info, error message is {0}".format(msg))
    server = server_name + "Url"
    master_host = res_data["attach"][server]
    if master_host is None or master_host is "":
        assert False, info_logger.error("There is no useful master server".format())
    info_logger.info("The master {0} is {1}".format(server_name, master_host))
    return master_host.replace('http://', '')


# 通过scaler modify_space接口修改space状态或者flavor_id
# modify_type为1：修改space的状态status
# modify_type为2：修改flavorId
def scaler_modify_space_step(scaler_client, space_id, modify_type, status=0, flavor_id=""):
    modify_type_name = "status" if modify_type == 1 else "flavor_id"
    modify_data = status if modify_type == 1 else flavor_id
    info_logger.info("[STEP] Scaler modify space {0} to {1}.".format(modify_type_name, modify_data))
    scaler_client.scaler_modify_space(space_id, modify_type, status, flavor_id)
    info_logger.info("[STEP] Scaler modify space {0} to {1} successfully!".format(modify_type_name, modify_data))
    return
