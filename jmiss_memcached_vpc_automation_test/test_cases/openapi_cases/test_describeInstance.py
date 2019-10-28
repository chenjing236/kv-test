import pytest
from jdcloud_sdk.services.memcached.apis.DescribeInstanceRequest import *
from steps.MemcachedOperation import *


class TestDescribeInstance:

    @pytest.mark.openapi
    def test_describeInstance(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        describeInstance(client, instance_id, instance_data, config)

    @pytest.mark.openapi
    def test_describeInstanceNotFound(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        resp = describe(client, "mc-xxxxxx", config)
        checkNotFound(resp)



