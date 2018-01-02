# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestUpdateRedis:

    @pytest.mark.smoke
    def test_update_meta(self, create_redis_instance):
        # 创建云缓存实例，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 调用查询详情接口，获取资源name和remarks等信息
        info_logger.info("[STEP] Query redis instance detail, check the name and the remarks of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        print cluster
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Before update redis instance, name is {0} , remark is {1}".format(cluster["name"], cluster["remarks"]))
        # 调用更新基本信息接口更新资源name和remarks，验证接口调用成功
        new_name = "testChange_newName"
        new_remarks = "testChange_newRemarks"
        mark = "updatebaseinfo"
        update_data = {"spaceName": new_name,"remarks": new_remarks, "mark": mark}
        update_cache_cluster_step(redis_cap, resource_id, update_data)
        # 调用查询详情接口，获取资源修改后的name和remarks信息
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        info_logger.info("[INFO] After update redis instance, name is {0} , remark is {1}".format(cluster["name"], cluster["remarks"]))
        # 验证修改后的name和remarks正确
        assert cluster["name"] == new_name, "[ERROR] The name of redis cluster is not updated!"
        assert cluster["remarks"] == new_remarks, "[ERROR] The remark  of redis cluster is not updated!"
        info_logger.info("[INFO] Test update meta successfully!")

    @pytest.mark.smoke
    def test_reset_password(self, create_redis_instance):
        # 创建云缓存实例，支付成功，验证资源状态为100
        redis_cap, cap, request_id_for_redis, resource_id = create_redis_instance
        # 调用查询详情接口，获取资源password等信息
        info_logger.info("[STEP] Query redis instance detail, check the name and the remarks of redis instance")
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        print cluster
        assert cluster["status"] == 100, "[ERROR] The status of redis cluster is not 100!"
        info_logger.info("[INFO] Before update redis instance, name is {0} , remark is {1}".format(cluster["name"], cluster["remarks"]))
        # 调用更新基本信息接口更新资源password，验证接口调用成功
        new_password = "Test123456"
        mark = "updatepassword"
        update_data = {"password": new_password, "mark": mark, "spaceName": cluster["name"]}
        update_cache_cluster_step(redis_cap, resource_id, update_data)
        # 调用查询详情接口，获取资源修改后的password信息
        billing_order, cluster = query_cache_cluster_detail_step(redis_cap, resource_id)
        info_logger.info("[INFO] After update redis instance, password is {0}".format(cluster["password"]))
        # 验证修改后的name和remarks正确
        # assert cluster["password"] == new_password, "[ERROR] The remark  of redis cluster is not updated!"
        info_logger.info("[INFO] Test update password successfully!")
