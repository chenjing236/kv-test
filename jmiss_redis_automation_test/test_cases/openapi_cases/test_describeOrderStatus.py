from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeOrderStatus:

    @pytest.mark.openapi
    def test_describeOrderStatus(self, init_instance, config):
        client, resp, instance_id = init_instance
        print "----------attention--------------"
        print config["request_id"]
        resp = query_order_status(config, config["request_id"], client)
        assertRespNotNone(resp)



