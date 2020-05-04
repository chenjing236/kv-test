from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestDescribeSpecConfig:

    @pytest.mark.cjdebug
    def test_describe_spec_config(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_spec_conifg(config, client)
        assertRespNotNone(resp)
        #assert (resp.result["instanceClasses"]).sort() == (config["instanceClasses"]).sort()
        #assert config["classTotalCount"] == resp.result["totalCount"]
