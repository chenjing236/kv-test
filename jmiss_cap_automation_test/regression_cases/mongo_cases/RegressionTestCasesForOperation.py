# -*- coding: utf-8 -*-
import pytest
import logging
from BasicTestCase import *
info_logger = logging.getLogger(__name__)

# 运营接口的测试用例
class TestSmokeCasesForOperation:
    # 运营系统，删除资源
    @pytest.mark.smoke
    def _delete_resource(self, config, instance_data, cap_http_client, mongo_http_client, cap_http_client):
	info_logger.info("[Scenario] Delete mongo instance using operation delete action")
	# 创建mongo实例,类型为包年包月的资源
	info_logger.info("[STEP] Create a mongo instance with yearly fee")
	resource_id, mongo_info = get_mongo_instance_created_step(config, instance_data, mongo_http_client, cap_http_client)
	info_logger.info("[INFO] The mongo instance %s is created", resource_id)
	# 删除包年包月资源
	delete_no_overdue_resource_step(config, instance_data, cap_http_client, resource_id)
	# 查看mongo实例列表
	mongo_info_list = query_mongo_dbs_step(config, instance_data, mongo_http_client)
	# 验证被删除的mongo实例不在列表中

    # 运营系统，删除未过期资源
    @pytest.mark.smoke
    def _deleteNoOverdueResource(self, config, instance_data, cap_http_client, mongo_http_client):
        print ""
        # 创建mongo实例,类型为包年包月的资源
        resource_id, mongo_info = get_mongo_instance_created_with_yearly_fee_step(config, instance_data, mongo_http_client, cap_http_client)
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
    @pytest.mark.smoke
    def test_modify_user_visibleF_flavor(self, config, instance_data, cap_http_client):
        info_logger.info("[Scenario] Enable/disable flavor info for the mongo")
        # 查看flavor规格信息
	flavor_info_list=get_flavor_list_step(config, instance_data, mongo_http_client)
	# 将enable的flavor规格修改为disale
	flavor_info = {"type":"", "cpu":"", "memory":"", "actionType":""}
	modify_user_visible_flavor_step(config, instance_data, cap_http_client, flavor_info)
	# 用disale的flavor创建mongo实例
	
	# 验证创建mongo实例失败
	# 将disable的flavor修改为enable
	# 用enable的flavor规格创建mongo实例
	# 验证创建mongo实例成功
	# 验证mongo实例的规格为enable的flaovr规格	
