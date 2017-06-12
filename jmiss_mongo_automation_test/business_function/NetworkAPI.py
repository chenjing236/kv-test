# encoding:utf-8

import logging
import time
from utils.HttpClient import *

logger_info = logging.getLogger(__name__)

class Network(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient

    # 创建VPC，返回VPC_id
    def create_vpc(self):
        vpc_name = "vpc-{0}-{1}-{2}".format(time.time(), self.data_obj["vpc_node"], self.data_obj["vpc_name_suffix"])
        vpc_args = "{\"name\":\"{0}\",\"tenant_id\":\"{1}\"}".format(vpc_name, self.data_obj["tenant_id"])
        vpc_id = self.httpClient.create_vpc(vpc_args)
        return vpc_id

    # 获取当前VPC绑定的VROUTER_ID
    def get_vrouter_by_vpc(self, vpc_id):
        vrouters_args = "{\"tenant_id\":\"{0}\",\"desc_offset\":\"{1}\"}".format(self.data_obj["tenant_id"], self.data_obj["vrouter_desc_offset"])
        vrouter_array = self.httpClient.get_vrouters_of_vpc(vrouters_args)
        #TODO，需要从当前用户的所有vrouter列表中过滤当前VPC绑定的vrouter
        return vrouter_id

    # 创建子网
    def create_subnet(self, vpc_id, vrouter_id):
        subnet_name = ""
        create_subnet_args = "{\"name\":\"{0}\",\"Cidr\":\"${cidr}\",\"tenant_id\":\"${tenant_id}\",\"vpc_id\":\"${vpc_id}\",\"route_table_id\":\"${router_id}\"}".format()
        subnet_id = self.httpClient.create_subnet(create_subnet_args)
        return subnet_id
