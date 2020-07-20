import pytest
from jmiss_redis_automation_test.utils.HttpClient import *
from jmiss_redis_automation_test.steps.FusionOpertation import *

class TestMiddleApi:

    @pytest.mark.middle
    def test_sellout_specified_mem(self, config):
        resp = query_spec_conifg(config)
        specs = resp.result["instanceSpec"]["instanceVersions"][0]["instanceTypes"][0]["specs"]
        before = None
        after = None
        for spec in specs:
            if str(spec["memoryGB"]) in str(config["maintain"]["middle"]["memoryGB"]) and spec["azs"] is not None:
                before = len(spec["azs"])
                print "azs" + str(len(spec["azs"]))
        # set up specified mem sell out for one az
        HttpClient.middle_sell_request_curl(config, False)
        resp = query_spec_conifg(config)
        specs = resp.result["instanceSpec"]["instanceVersions"][0]["instanceTypes"][0]["specs"]
        for spec in specs:
            if str(spec["memoryGB"]) in str(config["maintain"]["middle"]["memoryGB"]) and spec["azs"] is not None:
                after = len(spec["azs"])
                print "azs" + str(len(spec["azs"]))
        assert(before != after)
        HttpClient.middle_sell_request_curl(config, True)



if __name__ =="__main__":
    pytest.main(['test_middle_apis.py', '-s'])
