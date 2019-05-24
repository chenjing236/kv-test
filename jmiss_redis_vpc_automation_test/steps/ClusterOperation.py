# coding:utf-8
import time
import logging
from business_function.Cluster import *
from business_function.CFS import *
info_logger = logging.getLogger(__name__)


# 创建一个缓存云实例，返回缓存云实例的space_id
def create_instance_step(instance):
    print "\n"
    info_logger.info("[STEP] Create an instance including a master container and a slave container")
    res_data, password = instance.create_instance()
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to create an instance, error message is {0}".format(msg))
    attach = res_data["attach"]
    if attach is None or attach is "":
        info_logger.error("Response of creating an instance is incorrect")
        assert False, info_logger.error("Response of creating an instance is incorrect")
    space_id = attach["spaceId"]
    operation_id = attach["operationId"]
    info_logger.info("The instance {0} is created, its password is {1}".format(space_id, password))
    return space_id, operation_id, password


# 获取创建后的缓存云实例的信息
def get_detail_info_of_instance_step(instance, space_id):
    info_logger.info("[STEP] Get detail info of the instance {0}".format(space_id))
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg))
    attach = res_data["attach"]
    if attach is None or attach is "":
        info_logger.error("Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, info_logger.error("Response of getting detail information for the instance {0} is incorrect".format(space_id))
    assert attach["status"] == 100, info_logger.error("The cluster status is not 100!")
    assert attach["zone"] != 'clsdocker', info_logger.error("The cluster zone is clsdocker!")
    info_logger.info("Get the right detail info, the status of cluster {0} is 100".format(space_id))
    return attach


def get_operation_result_step(instance, space_id, operation_id):
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
        time.sleep(wait_time)
    if count >= retry_times:
        assert False, info_logger.error("The operation of instance is failed")
    if code != 0:
        assert False, info_logger.error("The operation of instance is failed, error_code = {0}".format(code))
    info_logger.info("Get the right operation result, create instance successfully")
    return True


def set_acl_step(instance, space_id):
    info_logger.info("[STEP] Set enable acl for the instance {0}".format(space_id))
    res_data = instance.set_acl(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of setting acl is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to set acl, error message is {0}".format(msg))
    info_logger.info("Set acl successfully!")


def set_system_acl_step(instance, space_id, enable):
    res_data = instance.set_system_acl(space_id, enable)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of setting system acl is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to set system acl, error message is {0}".format(msg))


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


# 删除redis资源
def delete_instance_step(instance, space_id):
    info_logger.info("[STEP] Delete the instance {0}".format(space_id))
    res_data = instance.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to delete the instance {0}, error message is {1}".format(space_id, msg))
    # 删除等待时间
    time.sleep(15)


# 对redis资源进行调整内存操作，包括扩容及缩容
def resize_instance_step(instance, space_id, flavor_id):
    # 执行resize扩容操作
    info_logger.info("[STEP] Resize the instance {0}".format(space_id))
    res_data = instance.resize_instance(space_id, flavor_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to resize an instance, error message is {0}".format(msg))
    attach = res_data["attach"]
    if attach is None or attach is "":
        info_logger.error("Response of resizing an instance is incorrect")
        assert False, info_logger.error("Response of resizing an instance is incorrect")
    operation_id = attach["operationId"]
    # 获取操作结果，判断扩容是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, info_logger.error("Get the right operation result, resize instance failed")
    # 获取capacity
    info_new = instance.get_instance_info(space_id)
    attach_new = info_new["attach"]
    status = attach_new["status"]
    flavor_id_new = attach_new["flavorId"]
    info_logger.info("Resize the instance finished")
    return status, flavor_id_new


# 对redis资源执行failover操作，包括主从版和集群版分片的主从资源
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
    info_logger.info("Success to delete container [{0}]".format(container_id))
    # 查询CFS的redis，查看epoch的值是否有变化
    res_data = cfs_client.get_meta(space_id)
    if res_data is None:
        assert False, info_logger.error("Cannot get topology information from cfs")
    epoch_new = res_data["epoch"]
    count = 0
    retry_times = container.conf_obj["retry_getting_topology_from_cfs"]
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


# 对redis资源执行rebuild-upgrade操作
def run_rebuild_upgrade_step(instance, space_id):
    res_data = instance.rebuild_upgrade_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to upgrade an instance, error message is {0}".format(msg))
    attach = res_data["attach"]
    if attach is None or attach is "":
        info_logger.error("Response of upgrading an instance is incorrect")
        assert False, info_logger.error("Response of upgrading an instance is incorrect")
    operation_id_upgrade = attach["operationId"]
    # 获取操作结果，判断repair是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id_upgrade)
    assert is_success is True, info_logger.error("Get the right operation result, rebuild-upgrade instance failed")
    info_logger.info("Run rebuild upgrade successfully, The space_id of upgrade instance is {0}".format(space_id))
    return True


# 对redis资源执行rebuild-repair操作
def run_rebuild_repair_step(instance, space_id, container, cfs_client):
    # 获取原有epoch
    masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
    # stop master and slave container
    container.stop_jcs_docker(masterDocker)
    container.stop_jcs_docker(slaveDocker)
    # check space status = 101
    detail_info = get_detail_info_of_instance_step(instance, space_id)
    status = detail_info["status"]
    retry_times = instance.conf_obj["retry_getting_topology_from_cfs"]
    wait_time = instance.conf_obj["wait_time"]
    count = 1
    while status != 101 and count < retry_times:
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        status = detail_info["status"]
        info_logger.info("Retry {0} get information of instance. Status of instance is {1}".format(count, status))
        count += 1
        time.sleep(wait_time)
    # run rebuild repair
    info_logger.info("Start to run rebuild repair")
    res_data = instance.rebuild_repair_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    operation_id_repair = res_data["attach"]["operationId"]
    assert code == 0, info_logger.error("It is failed to rebuild repair instance {0}, error message is {1}".format(space_id, msg))
    # 获取操作结果，判断repair是否成功
    get_operation_result_step(instance, space_id, operation_id_repair)
    info_logger.info("Run rebuild repair successfully")
    return True


# 对redis资源执行rebuild-clone操作
def run_rebuild_clone_step(instance, space_id):
    res_data = instance.rebuild_clone_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to clone an instance, error message is {0}".format(msg))
    attach = res_data["attach"]
    if attach is None or attach is "":
        info_logger.error("Response of cloning an instance is incorrect")
        assert False, info_logger.error("[ERROR] Response of cloning an instance is incorrect")
    space_id = attach["spaceId"]
    operation_id_clone = attach["operationId"]
    # 获取操作结果，判断repair是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id_clone)
    assert is_success is True, info_logger.error("Get the right operation result, rebuild-upgrade instance failed")
    info_logger.info("Run rebuild clone successfully, The space_id of clone instance is {0}".format(space_id))
    return space_id


# 对redis资源修改密码
def reset_password_step(instance, space_id, password):
    info_logger.info("[STEP] Start to reset password of the cluster")
    res_data = instance.reset_password(space_id, password)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of reset_password is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to reset password, error message is {0}".format(msg))
    info_logger.info("[INFO] Reset password successfully! The password is \"{0}\"".format(password))


# 查询列表
def get_clusters_step(instance):
    info_logger.info("[STEP] Get list information of instance")
    res_data = instance.get_clusters()
    if res_data is None or res_data is "":
        assert False, "Response of get_clusters is incorrect"
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, "It is failed to get clusters, error message is {0}".format(msg)
    return res_data["attach"]


# 分页查询列表
def get_filter_clusters_step(instance, filterName="", filterSpaceType="", filterStatus="", sortName="", sortRule="",
                             pageSize="", pageNum=""):
    info_logger.info("[STEP] Get filter list information of instance")
    filters = "filterName={0}&filterSpaceType={1}&filterStatus={2}&sortName={3}&sortRule={4}&pageSize={5}&" \
              "pageNum={6}".format(filterName, filterSpaceType, filterStatus, sortName, sortRule, pageSize, pageNum)
    res_data = instance.get_filter_clusters(filters)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of get_clusters is incorrect")
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get clusters, error message is {0}".format(msg))
    return res_data["attach"]


# 对redis资源更新基本信息
def update_meta_step(instance, space_id, name, remarks):
    info_logger.info("[STEP] Update the meta of the instance")
    res_data = instance.update_meta(space_id, name, remarks)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of update_meta is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to update meta, error message is {0}".format(msg))
    info_logger.info("Update meta successfully!")


# 查询redis资源实时内存信息
def get_realtime_info_step(instance, space_id):
    res_data = instance.get_realtime_info(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of get_realtime_info is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get realtime info, error message is {0}".format(msg))
    return res_data["attach"]


# 查询redis资源监控信息
def get_resource_info_step(instance, space_id, period="15m", frequency="3m"):
    res_data = instance.get_resource_info(space_id, period, frequency)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of get_resource_info is incorrect for the instance {0}".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get resource info, error message is {0}".format(msg))
    return res_data["attach"]


# query flavor id by config
def query_flavor_id_by_config_step(instance, cpu, memory, disk, max_connections, net):
    flavor = {"cpu": cpu, "memory": memory, "disk": disk, "max_connections": max_connections, "net": net}
    res_data = instance.query_flavor_id_by_config(flavor)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of query_flavor_id_by_config is incorrect for the flavor {0}".format(flavor))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to query flavorId by config, error message is {0}".format(msg))
    return res_data["attach"]


# query config id by config flavor
def query_config_by_flavor_id_step(instance, flavor_id):
    res_data = instance.query_config_by_flavor_id(flavor_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of query_config_by_flavor_id is incorrect for the flavor [{0}]".format(flavor_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to query config by flavorId, error message is {0}".format(msg))
    return res_data["attach"]


# modify instance config
def modify_instance_config_step(instance, space_id, propt):
    res_data = instance.modify_instance_config(space_id, propt)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of modify_instance_config is incorrect for the instance [{0}]".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to modify instance config, error message is {0}".format(msg))
    operation_id = res_data["attach"]["operationId"]
    # 获取操作结果，判断备份是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, info_logger.error("Get the right operation result, modify instance config failed")
    return True


# query backup list
def query_backup_list_step(instance, space_id, base_id):
    res_data = instance.query_backup_list(space_id, base_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of query_backup_list is incorrect for the instance [{0}]".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to query backup list, error message is {0}".format(msg))
    backups = res_data["attach"]["backups"]
    return backups


# create backup
def create_backup_step(instance, space_id):
    res_data = instance.create_backup(space_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error(
            "Response of create_backup is incorrect for the instance [{0}]".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to create backup, error message is {0}".format(msg))
    operation_id = res_data["attach"]["operationId"]
    # 获取操作结果，判断备份是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, info_logger.error("Get the right operation result, backup instance failed")
    base_id = operation_id
    return base_id


# create store
def create_restore_step(instance, space_id, base_id):
    res_data = instance.create_restore(space_id, base_id)
    if res_data is None or res_data is "":
        assert False, info_logger.error(
            "Response of create_restore is incorrect for the instance [{0}]".format(space_id))
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to createrestore, error message is {0}".format(msg))
    operation_id = res_data["attach"]["operationId"]
    # 获取操作结果，判断restore是否成功
    is_success = get_operation_result_step(instance, space_id, operation_id)
    assert is_success is True, info_logger.error("Get the right operation result, restore instance failed")
    return True


# 通过web get_cluster_info接口查询当前主CFS
def get_master_cfs_step(instance):
    info_logger.info("[STEP] To get master cfs.")
    res_data = instance.op_get_cluster_info()
    if res_data is None or res_data is "":
        assert False, info_logger.error("Response of op_get_cluster_info is incorrect".format())
    code = res_data["code"]
    msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("gbk")
    assert code == 0, info_logger.error("It is failed to get cluster op info, error message is {0}".format(msg))
    cfs_host = res_data["attach"]["cfsUrl"]
    if cfs_host is None or cfs_host is "":
        assert False, info_logger.error("There is no useful cfs".format())
    info_logger.info("The master cfs is {0}".format(cfs_host))
    return cfs_host.replace('http://', '')
