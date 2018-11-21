from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestModifyCacheInstanceClass:

    @pytest.mark.openapi
    def test_modifyCacheInstanceClass(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_class(config, instance_id, config["change_data"]["redis.m1.small.basic"], client)
        assertRespNotNone(resp)


