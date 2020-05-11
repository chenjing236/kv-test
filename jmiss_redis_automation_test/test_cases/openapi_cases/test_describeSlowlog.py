from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestDescribeSlowLog:
    @pytest.mark.slowlog
    def test_describeSlowlog(self, init_instance, config, instance_data):
        client, resp, instance_id = init_instance
        resp = query_instance(config, instance_id, client)
        assertRespNotNone(resp)
        validateResult(resp.result["cacheInstance"], config["instance"])
        resp = query_slow_log(config, instance_id)
        assertRespNotNone(resp)

        print("=====set up slow log via instance config========")
        resp = set_config(config, instance_id, config["instance_config_slowlog"], client)
        assertRespNotNone(resp)

        print("=======exec redis cli===========")
        instance = instance_data["create_standard_specified"][0]
        resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.checkAllCommand()

        resp = query_slow_log(config, instance_id)
        assertRespNotNone(resp)
