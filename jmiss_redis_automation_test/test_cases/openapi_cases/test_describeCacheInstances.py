from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeInstances:

    @pytest.mark.openapi
    def test_describeCacheInstances(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_instance_by_id(config, instance_id, client)
        assertInstance(resp, instance_id)




