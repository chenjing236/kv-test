from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestCreateInstance:

    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_createCacheInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        assert instance_id is not None
        assertRespNotNone(resp)
        time.sleep(150)




