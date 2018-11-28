import pytest
from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *

class TestDescribeInstanceNames:

    @pytest.mark.openapi
    def test_describeInstanceNames(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_instance_names(config, instance_id, client)
        assertRespNotNone(resp)
        print resp.result["data"][0]["resourceName"]
        print config["instance"]["cacheInstanceName"]
        print resp.result["data"][0]["serviceCode"]
        assert resp.result["data"][0]["resourceName"] == config["instance"]["cacheInstanceName"]
        assert resp.result["data"][0]["serviceCode"] == "redis"




