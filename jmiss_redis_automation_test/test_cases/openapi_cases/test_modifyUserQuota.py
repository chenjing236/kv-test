from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestModifyUserQuota:

    @pytest.mark.deprecated
    def test_modifyUserQuota(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_quota(config, 20, 2, client)
        assertRespNotNone(resp)



