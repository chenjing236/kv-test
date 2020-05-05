from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestDescribeSpecConfig:

    @pytest.mark.openapi
    @pytest.mark.regression
    @pytest.mark.cjdebug
    def test_describe_spec_config(self, config):
        resp = query_spec_conifg(config)
        assertRespNotNone(resp)

        specs = resp.result["instanceSpec"]["instanceVersions"][0]["instanceTypes"][0]["specs"]
        assert(len(specs) == len(config["specs"]))
        for spec in specs.sort():
            result = filter(lambda x: x['instanceClass'] == spec["instanceClass"], config["specs"])
            isExists = list(result)
            assert(isExists)

