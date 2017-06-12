# -*- coding: utf-8 -*- 

import json
import string
import logging

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

    def create_mongo_instance_with_param(self, data):
        create_args = CreateArgs(data)
        args_json = create_args.get_args_json()
        status, headers, res_data = self.httpClient.create_mongo_instance(data)
        assert status == 200, "[ERROR] HTTP Request is failed"
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

