from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestResetCacheInstancePassword:


    @pytest.mark.openapi
    @pytest.mark.smoke
    def test_resetCacheInstancePassword(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_password(config, instance_id, config["change_data"]["instancePassword"], client)
        assertRespNotNone(resp)

