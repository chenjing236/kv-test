from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.FusionOpertation import *


class TestDescribeSlowLog:
    @pytest.mark.slowlog
    def test_describeSlowlog(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_instance(config, instance_id, client)
        assertRespNotNone(resp)
        validateResult(resp.result["cacheInstance"], config["instance"])
        resp = query_slow_log(config, instance_id)
        assertRespNotNone(resp)

        print("================")
        resp = set_config(config, instance_id, config["instance_config_slowlog"], client)
        assertRespNotNone(resp)
        resp = query_slow_log(config, instance_id)
        assertRespNotNone(resp)
        