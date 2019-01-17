from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeInstanceClass:

    @pytest.mark.openapi
    def test_describeInstanceClass(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_class(config, client)
        assertRespNotNone(resp)
        assert (resp.result["instanceClasses"]).sort() == (config["instanceClasses"]).sort()
        assert config["classTotalCount"] == resp.result["totalCount"]




