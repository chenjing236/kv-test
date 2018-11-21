from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestModifyInstanceAttribute:


    @pytest.mark.openapi
    def test_modifyCacheInstanceAttribute(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_attribute(config, instance_id, config["change_data"]["cacheInstanceName"]
                               , config["change_data"]["cacheInstanceDescription"], client)
        assertRespNotNone(resp)
        assert resp.result["data"][0]["cacheInstanceName"] == config["change_data"]["cacheInstanceName"]
        assert resp.result["data"][0]["cacheInstanceName"] == config["change_data"]["cacheInstanceDescription"]