from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeInstances:

    @pytest.mark.openapi
    @pytest.mark.smoke
    def test_describeCacheInstances(self, init_instance, config):
        client, resp, instance_id = init_instance
        #根据id查询
        resp = query_instance_by_id(config, instance_id, client)
        assertInstance(resp, instance_id)
        #根据name查询
        #根据version查询
        #根据状态查询



