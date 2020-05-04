import pytest
from jmiss_redis_automation_test.utils.HttpClient import *


class TestMiddleApi:

    @pytest.mark.middle
    def test_sellout_specified_mem(self, config):
        # set up specified mem sell out for one az
        res = HttpClient.middle_sell_request(config, True)
        res = res.json()
        assert res[u'code'] is 200


if __name__ =="__main__":
    pytest.main(['test_middle_apis.py', '-s'])