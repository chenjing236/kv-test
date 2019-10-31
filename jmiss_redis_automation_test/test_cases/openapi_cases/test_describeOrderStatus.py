from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeOrderStatus:

    @pytest.mark.openapi
    @pytest.mark.regression
    def test_describeOrderStatus(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_order_status(config, config["request_id"], client)
        assertRespNotNone(resp)
        validateResult(resp.result, config["order_result"])
        assert resp.result["resourceIds"][0] == instance_id
        assert resp.result["total"] == 1
        assert resp.result["success"] == 1



