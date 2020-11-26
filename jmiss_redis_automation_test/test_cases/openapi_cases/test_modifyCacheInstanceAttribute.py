from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestModifyInstanceAttribute:


    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.stability
    @pytest.mark.jdstack
    def test_modifyCacheInstanceAttribute(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_attribute(config, instance_id, config["change_data"]["cacheInstanceName"]
                               , config["change_data"]["cacheInstanceDescription"], client)
        assertRespNotNone(resp)
        resp = query_instance(config, instance_id, client)
        assert resp.result["cacheInstance"]["cacheInstanceName"] == config["change_data"]["cacheInstanceName"]
        assert resp.result["cacheInstance"]["cacheInstanceDescription"] == config["change_data"]["cacheInstanceDescription"]