# coding:utf-8
from Container import *
from CFS import *
import json
import string
import random
import logging

logger_info = logging.getLogger(__name__)


# 创建缓存云实例API接口参数
class CreateArgs():
    def __init__(self, data):
        self.args_dict = data

    def to_json_string(self):
        return json.dumps(self.args_dict)

    def set_capacity(self, capacity):
        self.args_dict["capacity"] = capacity

    def set_zoneId(self, zoneId):
        self.args_dict["zoneId"] = zoneId

    def set_password(self, password):
        characters = string.ascii_letters + string.digits
        length = random.randint(0, 8)
        for i in range(length):
            password += characters[random.randint(0, len(characters) - 1)]
        # print "password = " + password
        self.args_dict["password"] = password

    def get_args_json(self):
        return self.args_dict


# 缓存云实例类
class Cluster(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient

    # 创建单实例缓存云实例
    def create_instance(self):
        zone_id = (self.conf_obj["version"] == "v2.0") and "0" or self.data_obj["zoneId"]
        data = {"spaceName": self.data_obj["spaceName"], "spaceType": self.data_obj["spaceType"],
                "zoneId": zone_id, "capacity": self.data_obj["capacity"],
                "quantity": self.data_obj["quantity"], "remarks": self.data_obj["remarks"],
                "availableZone": self.data_obj["availableZone"]}
        create_args = CreateArgs(data)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.create_cluster(args_json)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 创建单实例缓存云实例
    def create_instance_with_capacity(self, capacity):
        zone_id = (self.conf_obj["version"] == "v2.0") and "0" or self.data_obj["zoneId"]
        data = {"spaceName": self.data_obj["spaceName"], "spaceType": self.data_obj["spaceType"],
                "zoneId": zone_id, "capacity": self.data_obj["capacity"],
                "quantity": self.data_obj["quantity"], "remarks": self.data_obj["remarks"],
                "availableZone": self.data_obj["availableZone"]}
        create_args = CreateArgs(data)
        create_args.set_capacity(capacity)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.create_cluster(args_json)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 创建缓存云实例时设置密码
    def create_instance_with_password(self, password):
        data = {"spaceName": self.data_obj["spaceName"], "spaceType": self.data_obj["spaceType"],
                "zoneId": self.data_obj["zoneId"], "capacity": self.data_obj["capacity"],
                "quantity": self.data_obj["quantity"], "remarks": self.data_obj["remarks"], "password": password,
                "availableZone": self.data_obj["availableZone"]}
        create_args = CreateArgs(data)
        create_args.set_password(password)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.create_cluster(args_json)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data, args_json["password"]

    #删除单实例缓存云实例
    def delete_instance(self, spaceId):
        status, headers, res_data = self.httpClient.delete_cluster(spaceId)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取单实例缓存云实例的详细信息
    def get_instance_info(self, space_id):
        status, headers, res_data = self.httpClient.get_cluster(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取缓存云实例的拓扑结构
    def get_topology_of_instance(self, res_data, spaceId):
        msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("utf-8")
        attach = res_data["attach"]
        if attach == None or attach is "":
            assert False, "{0}".format(msg)
        shards = attach["shards"][0]
        instances = shards["instances"]
        instance_a = instances[0]
        instance_b = instances[1]
        #print "[INFO] Info of instance is {0}".format(instances)
        masterIp_a = instance_a["masterIp"]
        masterPort_a = instance_a["masterPort"]
        masterIp = masterIp_a
        masterPort = masterPort_a
        slaveIp = instance_a["ip"]
        slavePort = instance_a["port"]
        if masterIp_a == None:
            masterIp = instance_b["masterIp"]
            masterPort = instance_b["masterPort"]
            slaveIp = instance_b["ip"]
            slavePort = instance_b["port"]
        logger_info.info("[INFO] Master_Ip:Master_Port={0}:{1}, Slave_Ip:Slave_Port={2}:{3}".format(masterIp, masterPort, slaveIp, slavePort))
        return masterIp, masterPort, slaveIp, slavePort

    # 获取缓存云集群的拓扑结构
    def get_topology_of_cluster(self, res_data, spaceId):
        capa = int(self.data_obj["capacity"]) / 1024 / 1024
        shardNum = self.conf_obj["cluster_cfg"][str(capa)]
        logger_info.info("[INFO] The count of shards of cluster is {0}".format(shardNum))
        msg = json.dumps(res_data["msg"], ensure_ascii=False).encode("utf-8")
        attach = res_data["attach"]
        if attach is None or attach is "":
            assert False, "{0}".format(msg)
        shards = attach["shards"]
        shards_list = []
        for i in range(0, shardNum):
            instances = shards[i]["instances"]
            instance_a = instances[0]
            instance_b = instances[1]
            # print "[INFO] Info of instance is {0}".format(instances)
            masterIp_a = instance_a["masterIp"]
            masterPort_a = instance_a["masterPort"]
            masterIp = masterIp_a
            masterPort = masterPort_a
            slaveIp = instance_a["ip"]
            slavePort = instance_a["port"]
            if masterIp_a is None:
                masterIp = instance_b["masterIp"]
                masterPort = instance_b["masterPort"]
                slaveIp = instance_b["ip"]
                slavePort = instance_b["port"]
            shard = {"masterIp": masterIp, "masterPort": masterPort, "slaveIp": slaveIp, "slavePort": slavePort}
            shards_list.append(shard)
        return shards_list

    #扩容/缩容缓存云实例
    def resize_instance(self, space_id, zoneId, capacity):
        status, headers, res_data = self.httpClient.resize_cluster(space_id, zoneId, capacity)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #设置ACL访问规则
    def set_acl(self, space_id, ips):
        status, headers, res_data = self.httpClient.set_acl(space_id, ips)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取ACL访问规则
    def get_acl(self, space_id):
        status, headers, res_data = self.httpClient.get_acl(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # set system acl
    def set_system_acl(self, space_id, enable):
        status, headers, res_data = self.httpClient.set_system_acl(space_id, enable)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # reset password
    def reset_password(self, space_id, password):
        status, headers, res_data = self.httpClient.reset_password(space_id, password)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 获取操作结果
    def get_operation_result(self, space_id, operation_id):
        status, headers, res_data = self.httpClient.get_operation_result(space_id, operation_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 获取资源列表
    def get_clusters(self):
        status, headers, res_data = self.httpClient.get_clusters()
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 使用过滤条件查询缓存云列表
    def get_filter_clusters(self, filters):
        status, headers, res_data = self.httpClient.get_filter_clusters(filters)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 修改基本信息
    def update_meta(self, space_id, name, remarks):
        status, headers, res_data = self.httpClient.update_meta(space_id, name, remarks)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 获取资源实时使用信息
    def get_realtime_info(self, space_id):
        status, headers, res_data = self.httpClient.get_realtime_info(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # 获取资源监控信息
    def get_resource_info(self, space_id, period, frequency):
        status, headers, res_data = self.httpClient.get_resource_info(space_id, period, frequency)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # rebuild-repair
    def rebuild_repair_instance(self, space_id):
        status, headers, res_data = self.httpClient.rebuild_repair(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    # rebuild-clone
    def rebuild_clone_instance(self, space_id):
        data = {"spaceName": self.data_obj["spaceName"], "srcSpaceId": space_id, "remarks": self.data_obj["remarks"], "password": self.data_obj["password"]}
        create_args = CreateArgs(data)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.rebuild_clone(args_json)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data
