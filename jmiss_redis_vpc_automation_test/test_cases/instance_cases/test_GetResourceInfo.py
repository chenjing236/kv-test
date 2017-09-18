# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestGetResourceInfo:

    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.getresourceinfo
    def test_get_resource_info(self, created_instance):
        info_logger.info("[SCENARIO] Start to test get clusters")
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
        # 查看缓存云监控信息
        info_logger.info("[STEP3] Get resource info of the instance")
        resource_info = get_resource_info_step(instance, space_id)
        if resource_info is not None:
            info_logger.info(json.dumps(resource_info, ensure_ascii=False))
            xAxis = resource_info["xAxis"]
            series = resource_info["series"]
            assert len(xAxis) == 5 and len(series) == 5, "[ERROR] The response of get resource info is error!"
            for i in range(0, 5):
                assert len(series[i]["data"]) == 5, "[ERROR] The response of get resource info is error!"
            info_logger.info("[INFO] Get resource info successfully")
        else:
            info_logger.info("[INFO] API of get resource info is right, but there is no data of resource")
        # 查看缓存云实时信息
        info_logger.info("[STEP4] Get realtime info of the instance")
        realtime_info = get_realtime_info_step(instance, space_id)
        for i in range(3):
            if realtime_info is not None:
                info_logger.info(json.dumps(realtime_info, ensure_ascii=False))
                infos = realtime_info["infos"]
                assert infos[0]["spaceId"] == space_id and infos[0]["memUsed"] >= 0, "[ERROR] The response of get realtime info is error"
                info_logger.info("[INFO] Get realtime info successfully, memUsed of instance is {0} Byte".format(infos[0]["memUsed"]))
                break
            else:
                info_logger.info("[INFO] API of get realtime info is right, but there is no data of resource, wait for a moment")
                time.sleep(60)
                realtime_info = get_realtime_info_step(instance, space_id)
        info_logger.info("[INFO] Test get realtime info successfully")
