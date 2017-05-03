# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestGetList:

    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.getlist
    def test_get_redis_list(self, config, created_instance):
        info_logger.info("[SCENARIO] Start to access AP and to set/get key")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 查看缓存云实例详细信息
        info_logger.info("[STEP2] Get detailed information of the instance %s", space_id)
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        status = cluster_info["status"]
        name = cluster_info["name"]
        zoneId = cluster_info["zoneId"]
        info_logger.info("[INFO] Status of the instance %s is %s", space_id, status)
        # 验证缓存云实例状态，status=100创建成功
        assert status == 100
        # 查看缓存云实例列表
        info_logger.info("[STEP3] Get list information of instance")
        cluster_list = get_clusters_step(instance)
        assert cluster_list is not None, "[ERROR] Cluster list is none"
        for c in cluster_list:
            assert c["status"] != 102, "[ERROR] There is a cluster which status equals 102 in the cluster list"
            if c["space_id"] == space_id:
                # 验证列表页信息与详情页一致
                assert c["status"] == cluster_info["status"] and c["name"] == cluster_info["name"] and\
                        c["spaceType"] == cluster_info["spaceType"] and c["zoneId"] == cluster_info["zoneId"] and\
                        c["capacity"] == cluster_info["capacity"] and c["domain"] == cluster_info["domain"], "[ERROR] " \
                        "Info of cluster list is incorrect"
                info_logger.info("[INFO] Info of cluster list is correct")
                is_exist = True
        # 列表页不存在此资源
        assert is_exist is True, "[ERROR] The cluster {0} is not in cluster list".format(space_id)
        info_logger.info("[INFO] Test get clusters successfully")
