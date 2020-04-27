#!/bin/python
# coding:utf-8
from jmiss_redis_automation_test.steps.InstanceOperation import *

# 验证1G主从 有密码实例
# 验证2G主从 无密码实例
# 验证4G主从
# 验证8G主从
# ...
# 验证64G主从


@pytest.mark.intergration
@pytest.mark.createstandard
def test_specified_standard_createCacheInstance(self, config, instance_data, expected_data):
    instances = instance_data["create_standard_specified"]
    print("Standard instances count is %s" % len(instances))
    for i in range(len(instances)):
        client, _, instance_id = create_validate_instance(config, instances[i], expected_data)

        if instance_id is not None:
            delete_instance(config, instance_id, client)
