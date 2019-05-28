# coding:utf-8
from BasicTestCase import *


class TestUpdateMeta:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_update_meta(self, created_instance):
        info_logger.info("[SCENARIO] Start to test update meta")
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 查看缓存云实例详细信息
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        name = cluster_info["name"]
        # 修改名称
        time.sleep(3)
        new_name = name + "_new"
        update_meta_step(instance, space_id, new_name, "")
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        assert cluster_info["name"] == new_name, info_logger.error("Update name error!")
        remarks = cluster_info["remarks"]
        # 修改描述
        time.sleep(3)
        new_remarks = remarks + "_new"
        update_meta_step(instance, space_id, "", new_remarks)
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        assert cluster_info["remarks"] == new_remarks, info_logger.error("Update remarks error!")
