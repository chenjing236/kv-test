from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *

class TestInstanceBasecheck:
    @pytest.mark.basecheck
    def test_standard_base_check(self, config, instance_data, expected_data):
        expected_object = baseCheckPoint(expected_data["redis.s.micro.basic"], "1qaz2WSX")

        assert check_admin_proxy_redis_configmap("redis-iymph3d2st73", config, expected_object, 1)

    @pytest.mark.reset
    def test_modifySpecifedInstanceClass(self, config):
        resp = reset_class(config, "redis-24hu7ri9yx85", 'redis.s.small.basic', None, 2)
        assertRespNotNone(resp)
        instance = query_instance_recurrent(300, 6, "redis-24hu7ri9yx85", config, None)

