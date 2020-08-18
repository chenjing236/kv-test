from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestDescribeClientList:
    def test_describe_client_list(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_client_list(config, instance_id, client)
        assertRespNotNone(resp)
    	assert(resp.result["ips"] is None)

    def test_specified_client_list(self, config, instance_id):
        instance_id = instance_id
        resp = query_client_list(config, instance_id)
        assertRespNotNone(resp)
        assert(resp.result["ips"] is None)
