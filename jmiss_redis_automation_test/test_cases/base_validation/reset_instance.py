from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *


class TestModifyCacheInstanceClass:

    @pytest.mark.reset
    def test_modifyCacheInstanceClass(self, init_instance, config):
        resp = reset_class(config, "redis-iymph3d2st73", 'redis.s.small.basic', None, 1)
        assertRespNotNone(resp)
        instance = query_instance_recurrent(300, 6, "redis-iymph3d2st73", config, None)

