# -*- coding: utf-8 -*-
import pytest
import logging
from BasicTestCase import *
info_logger = logging.getLogger(__name__)

# 运营接口的测试用例
class TestSmokeCasesForOperation:
    # 运营系统，删除资源
    @pytest.mark.smoke
    def test_delete_resource(self, config, instance_data, cap_http_client, mongo_http_client, create_mongo_instance, create_mongo_instance_with_yearl_fee):
        # 创建mongo实例,类型为包年包月的资源
        resource_id, mongo_info = create_mongo_instance_with_yealy_fee
        # 查看资源列表
        request_id,mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证包年包月资源在列表中
        flag=False
        for item in mongo_info_list:
            if item["spaceId"] ==resource_id:
                flag=True
        assert flag==true,"[ERROR] the resource is not in the list"
        #  运营系统删除包年包月资源
        request_id = delete_resource_step(config, instance_data, cap_http_client, resource_id, instance_data["create_mongo_db_with_yearly_fee"]["feeType"])
        # 查看资源列表
        request_id,mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证被删除的资源不在资源列表信息中
        flag = False
        for item in mongo_info_list:
            if item["spaceId"] ==resource_id:
                flag=True
        assert flag==false,"[ERROR] the resource is in the list"
        # 创建mongo实例，类型为按计费类型
        resource_id, mongo_info = create_mongo_instance
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
    def test_deleteNoOverdueResource(self, config, instance_data, cap_http_client,mongo_http_client, create_mongo_instance, create_mongo_instance_with_yealy_fee):
        print ""
        # 创建mongo实例,类型为包年包月的资源
        resource_id, mongo_info = create_mongo_instance_with_yealy_fee
        # 运营系统删除资源
        request_id=delete_no_overdue_resource_step(config, instance_data, cap_http_client, resource_id, resource_type)
        # 查看资源列表
        request_id, mongo_info_list = get_mongo_dbs_step(config, instance_data, mongo_http_client)
        # 验证被删除的资源不在资源列表信息中
        flag = False
        for item in mongo_info_list:
            if item["spaceId"] == resource_id:
                flag = True
        assert flag == False, "[ERROR] the resource is in the list"

    # 运营修改用户可见flavor
    def test_modify_user_visibleF_flavor(self, config, instance_data, cap_http_client):
        print ""
        # 查看flavor规格信息
	    # 将enable的flavor规格修改为disale
	    # 用disale的flavor创建mongo实例
	    # 验证创建mongo实例失败
	    # 将disable的flavor修改为enable
	    # 用enable的flavor规格创建mongo实例
	    # 验证创建mongo实例成功
	    # 验证mongo实例的规格为enable的flaovr规格