from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *

class TestDescribeInternalSpec:
    @pytest.mark.openapi
    @pytest.mark.regression
    def test_describeInternalSpec(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_internal_spec(config, instance_id, client)
        assertRespNotNone(resp)

    def test_specified_internal_spec(self, config, instance_id):
        instance_id = instance_id
        resp = query_internal_spec(config, instance_id)
        assertRespNotNone(resp)
