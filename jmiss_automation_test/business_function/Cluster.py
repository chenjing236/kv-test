#!/usr/bin/python
# coding:utf-8
from Container import *
from CFS import *
#import sys
#sys.path.append("..")
#from utils.HttpClient import *
import json
import time

#创建缓存云实例API接口参数
class CreateArgs():
    def __init__(self, capacity=2097152, zoneid=1, remarks="jmiss_test", space_name="jmiss_test", space_type=1, quantity=1):
        self.args_dict = {"spaceName": space_name, "spaceType": space_type, "zoneId": zoneid, "capacity": capacity, "quantity": quantity,
         "remarks": remarks}

    def to_json_string(self):
        return json.dumps(self.args_dict)

    def set_capacity(self, capacity):
        self.args_dict["capacity"] = capacity

    def set_zoneId(self, zoneId):
        self.args_dict["zoneId"] = zoneId

#缓存云实例类
class Cluster(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient
        #self.httpClient = HttpClient(self.conf_obj["host"], self.conf_obj["pin"], self.conf_obj["auth_token"])

    #创建单实例缓存云实例
    def create_instance(self):
        data = {"spaceName": self.data_obj["spaceName"],"spaceType":self.data_obj["spaceType"],"zoneId":self.data_obj["zoneId"],"capacity":self.data_obj["capacity"],"quantity":self.data_obj["quantity"],"remarks":self.data_obj["remarks"]}
        status, headers, res_data = self.httpClient.create_cluster(data)
        retry_times = int(self.conf_obj["retry_creating_times"])
        count = 1
        while status != 200 and retry_times > 0:
            print "[INFO] Retry {0} creating an instance".format(count)
            status, headers, res_data = self.httpClient.create_cluster(data)
            retry_times -= 1
            count += 1
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #删除单实例缓存云实例
    def delete_instance(self, spaceId):
        status, headers, res_data = self.httpClient.delete_cluster(spaceId)
        retry_times = int(self.conf_obj["retry_deleting_times"])
        count = 1
        while status != 200 and retry_times > 0:
            print "[INFO] Retry {0} deleting an instance".format(count)
            status, headers, res_data = self.httpClient.delete_cluster(spaceId)
            retry_times -= 1
            count += 1
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取单实例缓存云实例的详细信息
    def get_instance_info(self, space_id):
        status, headers, res_data = self.httpClient.get_cluster(space_id)
        retry_times = int(self.conf_obj["retry_times"])
        count = 1
        while status != 200 and retry_times > 0:
            print "[INFO] Retry {0} getting information of  an instance".format(count)
            status, headers, res_data = self.httpClient.get_cluster(space_id)
            retry_times -= 1
            count += 1
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取缓存云实例的拓扑结构
    def get_topology_of_instance(self, res_data, spaceId):
        msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
        attach = res_data["attach"]
        if attach == None or attach is "":
            assert False, "{0}".format(msg)
        shards = attach["shards"][0]
        instances = shards["instances"]
        instance_a = instances[0]
        instance_b = instances[1]
        slaveIp = None
        slavePort = None
        masterIp_a = instance_a["masterIp"]
        masterIp = masterIp_a
        if masterIp_a == None:
            masterIp = instance_b["masterIp"]
            masterPort = instance_b["masterPort"]
            slaveIp = instance_b["ip"]
            slavePort = instance_b["port"]
        return masterIp, masterPort, slaveIp, slavePort

    def run_failover_container(self, space_id, containerIp, containerPort, docker_client, cfs_client):
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
        retry_times = int(config["retry_getting_topology_from_cfs"])
        count = 0;
        while epoch_new == epoch_origin and count <  retry_times:
            res_data = cfs_client.get_meta(space_id)
            if res_data == None:
                assert False, "[ERROR] Cannot get topology information from cfs"
            epoch_new = res_data["epoch"]
            count += 1
            time.sleep(int(self.conf_obj["wait_time"]))
        if count == retry_times:
            return False
        return True

    def set_acl(self, space_id, ips):
        status, headers, res_data = self.httpClient.set_acl(space_id, ips)
        retry_times = int(self.conf_obj["retry_times"])
        count = 1
        while status != 200 and retry_times > 0:
            print "[INFO] Retry {0} setting acl for an instance".format(count)
            status, headers, res_data = self.httpClient.set_acl(space_id, ips)
            retry_times -= 1
            count += 1
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    def get_acl(self, space_id):
        status, headers, res_data = self.httpClient.get_acl(space_id)
        retry_times = int(self.conf_obj["retry_times"])
        count = 1
        while status != 200 and retry_times > 0:
            print "[INFO] Retry {0} getting acl for an instance".format(count)
            status, headers, res_data = self.httpClient.get_acl(space_id)
            retry_times -= 1
            count += 1
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

if __name__ == "__main__":
    config_file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    config = json.load(open(config_file_path, 'r'))
    data_file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/data/instance_data.json"
    data = json.load(open(data_file_path, 'r'))
    cluster = Cluster(config, data, None)
    #创建缓存云实例
    print "[STEP1] Create an instance including a master container and a slave container"
    res_data = cluster.create_instance()
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to create an instance, error message is {0}".format(msg)
    attach = res_data["attach"]
    space_id = attach["spaceId"]
    print "[INFO] Space Id is {0}".format(space_id)

    #查询缓存云实例详细信息
    print "\n[STEP2] Get detailed information of instance {0}".format(space_id)
    res_data = cluster.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to get information of the instance {0}, error message is {1}".format(space_id, msg)
    attach = res_data["attach"]
    if attach == None or attach is "":
        assert False, "{0}".format(msg)
    status = attach["status"]
    capacity = attach["capacity"]
    count = 1
    while status != 100:
        res_data = cluster.get_instance_info(space_id)
        attach = res_data["attach"]
        status = attach["status"]
        attach = res_data["attach"]
        print "[INFO] Retry {0} get information of instance. Status of instance is {1}".format(count, status)
        count += 1
        time.sleep(5)
    print "[INFO] Status of instance is {0}".format(status)

    #获取缓存云实例的拓扑结构
    print "\n[STEP3] Get topology information of instance"
    masterIp, masterPort, slaveIp, slavePort = cluster.get_topology_of_instance(space_id)
    print "[INFO] Master Ip:Master Port  {0}:{1}".format(masterIp, masterPort)
    print "[INFO] Slave Ip:Slave Port  {0}:{1}".format(slaveIp, slavePort)

    #获取master container的大小
    file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    config = json.load(open(file_path, 'r'))
    container = Container(config)
    master_memory_size = container.get_memory_size_of_container(masterIp, masterPort)
    master_creation_time = container.get_creation_time_of_container(masterIp, masterPort)
    print "[INFO] Creation time of master container is {0}".format(master_creation_time)
    print "[INFO] Memory size of master container is {0} KB".format(master_memory_size)
    assert capacity == master_memory_size
    slave_memory_size = container.get_memory_size_of_container(slaveIp, slavePort)
    print "[INFO] Memory size of slave container is {0} KB".format(slave_memory_size)
    assert capacity == slave_memory_size

    #设置ACL访问规则
    print "\n[STEP4] Set acl for the instance {0}".format(space_id)
    ips = ["192.168.177.89", "192.168.169.51"]
    res_data = cluster.set_acl(space_id, ips)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to set acl, error message is {0}".format(msg)
    print "[INFO] It is successfull to set acl for the instance {0}".format(space_id)

    #获取访问规则
    print "\n[STEP5] Get acl for the instance {0}".format(space_id)
    res_data = cluster.get_acl(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to set acl, error message is {0}".format(msg)
    attach = res_data["attach"]
    ips = attach["ips"]
    print "[INFO] Ip list is {0}".format(ips)

    #master failover
    print "\n[STEP6] Run master failover"
    cfs_client = CFS(config)
    is_failover = cluster.run_failover_container(space_id, masterIp, masterPort,container, cfs_client)
    assert is_failover == True,"[ERROR] It is failed to run master failover"
    print "[INFO] It is succesfull to run master failover"
    res_data = cfs_client.get_meta(space_id)
    if res_data == None:
        assert False, "[ERROR] It is failed to get topology after running master failover."
    currentTopology = res_data["currentTopology"]
    master_ip_new, master_port_new, slaveIp_new, slavePort_new = cfs_client.get_topology_from_cfs(currentTopology)
    print "[INFO] master container info is {0}:{1}".format(master_ip_new, master_port_new)

    #删除缓存云实例
    print "\n[STEP7] Delete instance"
    res_data = cluster.delete_instance(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    assert code == 0, "[ERROR] It is failed to delete the instance {0}, error message is {1}".format(space_id, msg)
    res_data = cluster.get_instance_info(space_id)
    code = res_data["code"]
    msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
    if code == 0:
        print "[INFO] The instance {0} is deleted successfully".format(space_id)
    else:
        print "[INFO] The instance {0} is deleted successfully, message is {1}".format(space_id, msg)
