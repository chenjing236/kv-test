#!/bin/python
# coding:utf-8
from jmiss_redis_automation_test.steps.InstanceOperation import *

# 验证16集群 有密码实例
# 验证32G集群 无密码实例
# 验证64G集群
# ...
# 2T集群


class TestCreateClusterIntergration:

    @pytest.mark.intergration
    @pytest.mark.createcluster
    def test_specified_cluster_createCacheInstance(self, config, instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        print("Cluster instances count is %s" % len(instances))
        for i in range(len(instances)):
            client, _, instance_id = create_validate_instance(config, instances[i], expected_data)

            if instance_id is not None:
                delete_instance(config, instance_id, client)

