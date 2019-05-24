# coding:utf-8
from BasicTestCase import *


class TestGetFilterList:
    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_redis_list(self, created_instance):
        # 创建缓存云实例，创建成功
        space_id, instance, password = created_instance
        # 查看缓存云实例详细信息
        cluster_info = get_detail_info_of_instance_step(instance, space_id)
        # 根据过滤条件查询缓存云实例列表
        attach = get_filter_clusters_step(instance, filterStatus=100)
        spaces = attach["spaces"]
        total = attach["total"]
        assert total == len(spaces) and spaces is not None, "Cluster list is none"
        is_exist = False
        for c in spaces:
            assert c["status"] != 102, info_logger.error("There is a cluster which status equals 102 in the cluster list")
            if c["spaceId"] == space_id:
                # 验证列表页信息与详情页一致
                assert c["status"] == cluster_info["status"] and c["name"] == cluster_info["name"] and\
                        c["spaceType"] == cluster_info["spaceType"] and c["zone"] == cluster_info["zone"] and\
                        c["capacity"] == cluster_info["capacity"] and c["domain"] == cluster_info["domain"] and\
                        c["flavorId"] == cluster_info["flavorId"], "[ERROR] Info of cluster list is incorrect"
                is_exist = True
        # 列表页不存在此资源时
        assert is_exist is True, info_logger.error("The cluster {0} is not in cluster list".format(space_id))
