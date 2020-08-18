from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestDescribeClientIpDetail:
    def test_describe_client_ip_detail(self, init_instance, config):
        client, resp, instance_id = init_instance
        ip = '127.0.0.1'
        resp = query_client_ip_detail(config, instance_id, ip, client)
        assertRespNotNone(resp)
        assert(resp.result["details"] is None)
   

    def test_specified_client_ip_detail(self, config, instance_id):
        instance_id = instance_id
        ip = '127.0.0.1'
        resp = query_client_ip_detail(config, instance_id, ip)
        assertRespNotNone(resp)
        assert(resp.result["details"] is None)
