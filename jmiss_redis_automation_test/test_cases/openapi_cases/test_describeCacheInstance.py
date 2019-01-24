from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *

class TestDescribeInstance:

    @pytest.mark.openapi
    @pytest.mark.smoke
    def test_describeCacheInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_instance(config, instance_id, client)
        assertRespNotNone(resp)
        validateResult(resp.result["cacheInstance"], config["instance"])
        existResult(resp.result["cacheInstance"], config["exist_data"])

    @pytest.mark.openapi
    def test_describeCacheInstanceNotFound(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_instance(config, "redis-xxxxxx", client)
        checkNotFound(resp)


