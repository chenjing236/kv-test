# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestUpdateMeta:
    @pytest.mark.updatemeta
    def test_update_meta(self, created_instance):
        info_logger.info("[SCENARIO] Start to test update meta")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the instance {0}".format(space_id))
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        status = cluster_info["status"]
        info_logger.info("[INFO] Status of the instance {0} is {1}".format(space_id, status))
        name = cluster_info["name"]
        info_logger.info("[INFO] The name of the instance is {0}".format(name))
        # 修改名称
        info_logger.info("[STEP3] Update the name of the instance")
        time.sleep(3)
        new_name = name + "_new"
        update_meta_step(instance, space_id, new_name, "")
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        assert cluster_info["name"] == new_name, "[ERROR] Update name error!"
        info_logger.info("[INFO] Update name successfully, new name is {0}".format(new_name))
        remarks = cluster_info["remarks"]
        info_logger.info("[INFO] The remarks of the instance is {0}".format(remarks))
        # 修改描述
        info_logger.info("[STEP4] Update the remarks of the instance")
        time.sleep(3)
        new_remarks = remarks + "_new"
        update_meta_step(instance, space_id, "", new_remarks)
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        assert cluster_info["remarks"] == new_remarks, "[ERROR] Update remarks error!"
        info_logger.info("[INFO] Update remarks successfully, new remarks is {0}".format(new_remarks))
        info_logger.info("[INFO] Test Update meta successfully")
