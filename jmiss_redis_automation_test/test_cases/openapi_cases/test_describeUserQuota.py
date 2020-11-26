from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeUserQuota:

    @pytest.mark.openapi
    @pytest.mark.regression
    @pytest.mark.jdstack
    def test_describeUserQuota(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_quota(config, client)
        assertRespNotNone(resp)
        validateResult(resp.result["quota"], config["quota"])





