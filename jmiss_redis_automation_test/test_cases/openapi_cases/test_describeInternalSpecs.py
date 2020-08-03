from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *

class TestDescribeInternalSpecs:

    def test_describeInternalSpecs(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_internal_specs(config, instance_id, client)
        assertRespNotNone(resp)
        #validateResult(resp.result["cacheInstance"], config["instance"])
        #existResult(resp.result["cacheInstance"], config["exist_data"])
