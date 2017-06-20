# -*- coding: utf-8 -*-
import pytest
import logging
import time
from BasicTestCase import *
info_logger = logging.getLogger(__name__)

# 运营接口的测试用例
class TestSmokeCasesForOperation:
    # 运营系统，删除资源
    @pytest.mark.smoke
    def test_delete_resource(self, config, instance_data, cap_http_client, mongo_http_client):
        # 创建mongo实例,类型为包年包月的资源
        resource_id, mongo_info = create_mongo_instance_yearly_fee_step(config, instance_data, mongo_http_client, cap_http_client)
        # 查看资源列表
        request_id,mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证包年包月资源在列表中
        flag=False
        for item in mongo_info_list:
            if item["spaceId"] ==resource_id:
                flag=True
        assert flag==True,"[ERROR] the resource is not in the list"
        #  运营系统删除包年包月资源
        request_id = delete_resource_step(config, instance_data, cap_http_client, resource_id, instance_data["create_mongo_db_with_yearly_fee"]["feeType"])
        # 查看资源列表
        request_id,mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证被删除的资源不在资源列表信息中
        flag = False
        for item in mongo_info_list:
            if item["spaceId"] ==resource_id:
                flag=True
        assert flag==False,"[ERROR] the resource is in the list"
        # 创建mongo实例，类型为按计费类型
        resource_id, mongo_info = create_mongo_instance_param_step(config, instance_data, mongo_http_client,cap_http_client)
        # 运营系统删除按配置类型
        request_id = delete_resource_step(config, instance_data, cap_http_client, resource_id,instance_data["create_mongo_db"]["feeType"])
        # 查看资源列表
        request_id, mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证被删除的资源不在资源列表信息中
        flag = False
        for item in mongo_info_list:
            if item["spaceId"] == resource_id:
                flag = True
        assert flag==False,"[ERROR] the resource is in the list"

    # 运营系统，删除未过期资源
    @pytest.mark.smoke
    def test_deleteNoOverdueResource(self, config, instance_data, cap_http_client,mongo_http_client):
        print ""
        # 创建mongo实例,类型为包年包月的资源
        resource_id, mongo_info = create_mongo_instance_yearly_fee_step
        # 运营系统删除资源
        request_id=delete_no_overdue_resource_step(config, instance_data, cap_http_client, resource_id)
        time.sleep(5)
        # 查看资源列表
        request_id, mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证被删除的资源不在资源列表信息中
        flag = False
        for item in mongo_info_list:
            if item["spaceId"] == resource_id and item["status"] == 100:
                flag = True
        assert flag == False, "[ERROR] the resource is in the list"

    # 运营修改用户可见flavor
    def test_modify_user_visibleF_flavor(self, config, instance_data, mongo_http_client,cap_http_client):
        # 查看flavor规格信息
        request_id, flavor_info_list=get_flavor_list_step(config,instance_data,mongo_http_client)
	    # 将enable的flavor规格修改为disale
        flavorDetail=flavor_info_list[0]
        flavor_info={"type":"mongodb","cpu":flavorDetail["cpu"],"memory":flavorDetail["memory"],"actionType":-1}
        request_id=modify_user_visible_flavor_step(config,instance_data,cap_http_client,flavor_info)
	    # 验证disale的flavor不存在
        request_id, flavor_info_list2 = get_flavor_list_step(config, instance_data, mongo_http_client)
        flavor_exist=False
        for item in flavor_info_list2:
            if item["cpu"] == flavorDetail["cpu"] and item["memory"] == flavorDetail["memory"]:
                flavor_exist=True
        assert flavor_exist == False, "[ERROR] modify user visible flavor exist"
	    # 将disable的flavor修改为enable
        flavor_info = {"type": "mongodb", "cpu": flavorDetail["cpu"], "memory": flavorDetail["momory"],"actionType": 1}
        request_id = modify_user_visible_flavor_step(config, instance_data, cap_http_client, flavor_info)
        # 验证flavor存在
        request_id, flavor_info_list3 = get_flavor_list_step(config, instance_data, mongo_http_client)
        flavor_exist = False
        for item in flavor_info_list3:
            if item["cpu"] == flavorDetail["cpu"] and item["memory"] == flavorDetail["memory"]:
                flavor_exist = True
        assert flavor_exist == True, "[ERROR] modify user visible flavor not exist"
