# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import logging
import time
from business_function.Cluster import *
from utils.MongoClient import *

logger_info = logging.getLogger(__name__)

#创建一个mongo实例，返回mongo实例的space_id
def create_mongo_instance_step(config, instance_data, http_client):
    instance= Cluster(config, instance_data, http_client)
    res_data = instance.create_mongo_instance(instance.data_obj["vpc_id"], instance.data_obj["subnetId"])
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to create an instance of mongo, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of creating an instance is incorrect")
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    return space_id

#创建一个运行状态的实例，即100状态的mongo实例
def create_available_mongo_instance_step(config, instance_data, http_client):
    logger_info.info("[STEP] Create a mongo instance")
    space_id = create_mongo_instance_step(config, instance_data, http_client)
    logger_info.info("[INFO] The mongo %s is being created", space_id)
    logger_info.info("[STEP] Get status of the mongo instance %s", space_id)
    status = get_status_of_instance_step(config, instance_data, http_client, space_id)
    logger_info.info("[INFO] The status of the mongo %s is %s", space_id, status)
    assert status == 100, "[ERROR] Instance {0} is unavailable".format(space_id)
    time.sleep(int(instance_data["wait_short_time"]))
    return space_id

#获取mongo实例修改名称后的实例
def get_changed_name_of_mongo_instance_step(config, instance_data, http_client, space_id, name_changed):
    change_name_for_mongo_instance_step(config, instance_data, http_client, space_id, name_changed)
    logger_info.info("[STEP] Get the name changed for the mongo instance %s", space_id)
    mongo_info = get_detail_info_of_instance_step(config, instance_data, http_client, space_id)
    logger_info.info("[VERIFICATION] The name changed is the same with the specific name")
    assert name_changed == mongo_info["name"], "[ERROR] It is failed to change name for the mongo instance {0}".format(space_id)
    return mongo_info

#根据指定的flavor信息，创建一个mongo实例
def create_mongo_instance_with_flavor_step(config, instance_data, http_client, flavor_id):
    instance= Cluster(config, instance_data, http_client)
    res_data = instance.create_mongo_instance_with_flavor(flavor_id, instance.data_obj["vpc_id"], instance.data_obj["subnetId"])
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to create an instance of mongo, error message is {0}".format(msg)
    attach = res_data["attach"]
    if attach is None or attach is "":
        logger_info.error("[ERROR] Response of creating an instance is incorrect")
        assert False, "[ERROR] Response of creating an instance is incorrect"
    space_id = attach["spaceId"]
    return space_id

#获取mongo实例的状态
def get_status_of_instance_step(config, instance_data, http_client, space_id):
    retry_times = int(config["retry_getting_info_times"])
    wait_time = int(config["wait_time"])
    instance= Cluster(config, instance_data, http_client)
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    status = attach["status"]
    count = 1
    while status != 100 and count < retry_times:
        res_data = instance.get_instance_info(space_id)
        if res_data is None or res_data is "":
            logger_info.error("[ERROR] It is failed to get topology from detail information of the instance %s.", space_id)
            assert False, "[ERROR] It is failed to get topology from detail information of the instance {0}.".format(space_id)
        attach = res_data["attach"]
        status = attach["status"]
        print "[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status)
        count += 1
        time.sleep(wait_time)
    return status

#删除mongo资源后获取mongo资源的状态
def get_status_of_deleted_instance_step(config, instance_data, http_client, space_id):
    retry_times = int(config["retry_getting_info_times"])
    wait_time = int(config["wait_time"])
    instance= Cluster(config, instance_data, http_client)
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert 10114 == code, "[ERROR] The space [{0}] of mongo cannot be delete, and error message is {1}".format(space_id, msg)
    status = 102
    return status

#修改mongo实例的名称
def change_name_for_mongo_instance_step(config, instance_data, http_client, space_id, space_name):
    instance= Cluster(config, instance_data, http_client)
    res_data = instance.change_name_for_mongo_instance(space_id, space_name)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to change name for the instance of mongo {0}, error message is {1}".format(space_id, msg)

#获取mongo实例的信息
def get_detail_info_of_instance_step(config, instance_data, http_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    return attach

#获取mongo的拓扑结构
def get_topology_of_mongo_step(config, instance_data, http_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_topology_of_mongo(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        logger_info.error("[ERROR] Response of getting detail information for the instance %s is incorrect", space_id)
        assert False, "[ERROR] Response of getting detail information for the instance {0} is incorrect".format(space_id)
    return attach

#删除mongo实例
def delete_instance_step(config, instance_data, http_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to delete the instance {0}, error message is {1}".format(space_id, msg)
    #time.sleep(int(instance_data["wait_time"]))

#获取操作结果
def get_results_of_operation_step(config, instance_data, http_client, space_id, operation_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_results_of_operation(space_id, operation_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to delete the instance {0}, error message is {1}".format(space_id, msg)

#从数据库中获取mongo实例的副本集关系
def get_replica_info_from_instance_step(config, instance_data, http_client, mysql_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    container_1, container_2, container3 = instance.get_results_of_operation(mysql_client, space_id)
    return container_1, container_2, container3

#获取实时信息
def get_real_time_info_step(config, instance_data, http_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_real_time_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get the real time info for the instance {0}, error message is {1}".format(space_id, msg)
    if None == res_data["attach"]:
	#assert False, "[ERROR] There is no real time info, and error message is {0}".format(msg)
	return msg
    return res_data["attach"]["infos"][0]

#获取监控信息
def get_monitor_info_step(config, instance_data, http_client, space_id):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_monitor_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get the real time info for the instance {0}, error message is {1}".format(space_id, msg)
    if None == res_data["attach"]:
        #assert False, "[ERROR] There is no real time info, and error message is {0}".format(msg)
        return msg
    return res_data["attach"]["infos"][0]

#分页过滤mongo实例信息
def get_clusters_by_page_step(config, instance_data, http_client, filter_name, page_size, page_num):
    instance = Cluster(config, instance_data, http_client)
    res_data = instance.get_clusters_by_page(filter_name, page_size, page_num)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"]).decode('unicode-escape')
    assert code == 0, "[ERROR] It is failed to get the real time info for the instance {0}, error message is {1}".format(space_id, msg)
    clusters = res_data["attach"]
    if None == clusters:
	assert Flase, "[ERROR] There is no matched mongo instance, and the error message is %s".format(msg)
    return clusters
