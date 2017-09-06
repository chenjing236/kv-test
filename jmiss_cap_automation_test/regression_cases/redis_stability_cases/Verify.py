# -*- coding: utf-8 -*-

from BasicTestCase import *

logger_info = logging.getLogger(__name__)

def verufy(clusters, cluster_info, resource_id):
    for cluster in clusters:
        assert cluster["status"] != 102, "[ERROR] There is a cluster which status equals 102 in the cluster list"
        if cluster["spaceId"] == resource_id:
            # 验证列表页信息与详情页一致
            assert cluster["status"] == cluster_info["status"] and cluster["name"] == cluster_info["name"] and \
                   cluster["spaceType"] == cluster_info["spaceType"] and cluster["zoneId"] == cluster_info["zoneId"] and \
                   cluster["capacity"] == cluster_info["capacity"] and cluster["domain"] == cluster_info[
                "domain"], "[ERROR] Info of cluster list is incorrect"
            is_exist = True
    assert is_exist is True, "[ERROR] The cluster {0} is not in cluster list".format(resource_id)
