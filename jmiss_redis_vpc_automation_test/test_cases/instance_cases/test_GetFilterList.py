# coding:utf-8
import pytest
from BasicTestCase import *

# info_logger = logging.getLogger(__name__)


class TestGetFilterList:
    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.getlist
    def test_get_redis_list(self, created_instance):
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
        # 根据过滤条件查询缓存云实例列表
        info_logger.info("[STEP3] Get filter list information of instance")
        attach = get_filter_clusters_step(instance)
        spaces = attach["spaces"]
        total = attach["total"]
        assert total == len(spaces) and spaces is not None, "[ERROR] Cluster list is none"
        for c in spaces:
            assert c["status"] != 102, "[ERROR] There is a cluster which status equals 102 in the cluster list"
            if c["spaceId"] == space_id:
                # 验证列表页信息与详情页一致
                assert c["status"] == cluster_info["status"] and c["name"] == cluster_info["name"] and\
                        c["spaceType"] == cluster_info["spaceType"] and c["zone"] == cluster_info["zone"] and\
                        c["capacity"] == cluster_info["capacity"] and c["domain"] == cluster_info["domain"] and\
                        c["flavorId"] == cluster_info["flavorId"], "[ERROR] Info of cluster list is incorrect"
                info_logger.info("[INFO] Info of cluster list is correct, status={0}, "
                                 "name={1}, spaceType={2}, zone={3}, capacity={4}, domain={5}, "
                                 "flavorId={6}".format(c["status"], c["name"], c["spaceType"],
                                                       c["zone"], c["capacity"], c["domain"], c["flavorId"]))
                is_exist = True
        # 列表页不存在此资源时
        assert is_exist is True, "[ERROR] The cluster {0} is not in cluster list".format(space_id)
        info_logger.info("[INFO] Test get clusters successfully")
