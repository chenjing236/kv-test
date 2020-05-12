from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestDescribeSpecConfig:

    @pytest.mark.openapi
    @pytest.mark.regression
    @pytest.mark.cjdebug
    def test_describe_spec_config(self, config, instance_data):
        resp = query_spec_conifg(config)
        assertRespNotNone(resp)

        specs = resp.result["instanceSpec"]["instanceVersions"][0]["instanceTypes"][0]["specs"]
        assert(len(specs) == len(instance_data["specs"]))
        for spec in specs:
            result = filter(lambda x: x['instanceClass'] == spec["instanceClass"], instance_data["specs"])
            isExists = list(result)
            assert(isExists)

