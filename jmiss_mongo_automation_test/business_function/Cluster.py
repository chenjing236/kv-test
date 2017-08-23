# -*- coding: utf-8 -*- 
import json
import string
import logging
from utils.MySqlClient import *

logger_info = logging.getLogger(__name__)

#创建mongo的参数bean
class CreateArgs():
    def __init__(self, data):
        self.args_dict = data
    def to_json_string(self):
        return json.dumps(self.args_dict)
    def get_args_json(self):
        return self.args_dict
    def set_vpc(self, vpc_id):
        self.args_dict["vpc_id"] = vpc_id
    def set_subnet(self, subnetId):
        self.args_dict["subnetId"] = subnetId
    def set_flavor(self, flavorId):
        self.args_dict["flavorId"] = flavorId
    def set_password(self, password):
        self.args_dict["password"] = password
    def set_osUserInfo(self, osUserInfo):
        self.args_dict["osUserInfo"] = osUserInfo

#此处待重构时，用工厂模式，创建不同资源实例
class Cluster(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient

    def init_mysql_client(self, mysql_client):
	self.mysql_client = mysql_client

    def create_mongo_instance_with_param(self, data):
        create_args = CreateArgs(data)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.create_mongo_instance(data)
	msg = json.dumps(res_data["msg"],ensure_ascii=False).encode("gbk")
        assert status == 200, "[ERROR] HTTP Request is failed, the error message is {0}".format(msg)
        return res_data

    #创建mongo实例，参数默认
    def create_mongo_instance(self, vpc_id, subnetId):
        #一个mongo实例包括一个primary container，一个secondary container，一个hidden container
        spaceType = 1
        data = {"vpcId": vpc_id, "subnetId": subnetId,"flavorId":self.data_obj["flavorId"],"password": self.data_obj["password"],"spaceType": spaceType,"dbVersion": self.data_obj["dbVersion"],"osUserInfo": self.data_obj["osUserInfo"]}
        return self.create_mongo_instance_with_param(data)

    #创建mongo实例，指定flavor_id
    def create_mongo_instance_with_flavor(self, flavorId, vpc_id, subnetId):
        #一个mongo实例包括一个primary container，一个secondary container，一个hidden container
        spaceType = 1
        data = {"vpcId": vpc_id, "subnetId": subnetId,"flavorId": flavorId, "password": self.data_obj["password"],"spaceType": spaceType,"dbVersion": self.data_obj["dbVersion"],"osUserInfo": self.data_obj["osUserInfo"]}
        return self.create_mongo_instance_with_param(data)

    #创建mongo实例，指定password
    def create_mongo_instance_with_password(self, password, vpc_id, subnetId):
        #一个mongo实例包括一个primary container，一个secondary container，一个hidden container
        spaceType = 1
        data = {"vpcId": vpc_id, "subnetId": subnetId,"flavorId": data_obj["flavorId"],"password": self.data_obj["password"],"spaceType": spaceType,"dbVersion": self.data_obj["dbVersion"],"osUserInfo": self.data_obj["osUserInfo"]}
        return self.create_mongo_instance_with_param(data)

    #创建mongo实例，指定flavor_id和password
    def create_mongo_instance_with_flavor_and_password(self, flavorId, password, vpc_id, subnetId):
        #一个mongo实例包括一个primary container，一个secondary container，一个hidden container
        spaceType = 1
        data = {"vpcId": vpc_id, "subnetId": subnetId,"flavorId": self.data_obj["flavorId"],"password": self.data_obj["password"],"spaceType": spaceType,"dbVersion": self.data_obj["dbVersion"],"osUserInfo": self.data_obj["osUserInfo"]}
        return self.create_mongo_instance_with_param(data)

    #修改mongo名称
    def change_name_for_mongo_instance(self, space_id, space_name):
	data = {"spaceName":space_name}
	status, headers, res_data = self.httpClient.updatemeta_mongo_name(space_id, data)
	assert status == 200, "[ERROR] HTTP Request is failed"
	return res_data

    #删除mongo实例
    def delete_instance(self, spaceId):
        status, headers, res_data = self.httpClient.delete_mongo_instance(spaceId)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取mongo实例详细信息
    def get_instance_info(self, space_id):
        status, headers, res_data = self.httpClient.get_mongo_detail_info(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取mongo拓扑信息
    def get_topology_of_mongo(self, space_id):
        status, headers, res_data = self.httpClient.get_topology_of_mongo(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #从数据库instance表中获取mongo拓扑信息
    def get_results_of_operation(self, mysql_client, space_id):
	self.init_mysql_client(mysql_client)
	ins = self.mysql_client.get_instances(space_id)
	assert len(ins) == 3, "[ERROR] The replica info is incomplete"
	#container_1 = {"docker_id":ins[0][0], "host_ip":ins[0][1], "domain":ins[0][2], "instance_ip":ins[0][3]}
	#container_2 = {"docker_id":ins[1][0], "host_ip":ins[1][1], "domain":ins[1][2], "instance_ip":ins[1][3]}
	#container_3 = {"docker_id":ins[2][0], "host_ip":ins[2][1], "domain":ins[2][2], "instance_ip":ins[2][3]}
        #return container_1, container_2, container_3
	return ins

    #获取实时信息
    def get_real_time_info(self, space_id):
        status, headers, res_data = self.httpClient.get_real_time_info(space_id)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取监控信息
    def get_monitor_info(self, space_id):
	#data="period={0}m&frequency={1}m&role={2}".format(self.data_obj["monitor_param"]["period"], self.data_obj["monitor_param"]["frequency"], self.data_obj["monitor_param"]["role"])
	data = space_id + "?period=15m&frequency=1m&role=primary"
        status, headers, res_data = self.httpClient.get_monitor_info(space_id, data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #分页查询列表
    def get_clusters_by_page(self, filter_name, page_size, page_num):
        data = "filterName={0}&filterSpaceType=1&filterStatus=100&sortName=&sortRule=desc&pageSize={1}&pageNum={2}".format(filter_name, page_size, page_num)
        status, headers, res_data = self.httpClient.get_clusters_by_page(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #获取mongo列表信息
    def get_mongo_instance_list(self):
        status, headers, res_data = self.httpClient.get_mongo_instance_list()
        assert status == 200, "[ERROR] HTTP Request is failed"
        return res_data

    #手动创建备份
    def generate_backup_for_mongo(self,space_id):
        data = {"spaceId": space_id}
        status,headers,res_data = self.httpClient.generate_backup_for_mongo(data)
        assert status == 200,"[ERROR] HTTP Request is failed"
        return res_data

    def get_list_of_backup(self,space_id):
        data = space_id + "?startTime=&endTime=&pageNum=1&pageSize="
        status,headers,res_data = self.httpClient.get_list_of_backup(data)
        assert status == 200,"[ERROR] HTTP Request is failed"
        return res_data

    def get_backup_info(self,mysql_client,operation_id):
        self.init_mysql_client(mysql_client)
        ins = self.mysql_client.get_backup_info(operation_id)
        return ins
