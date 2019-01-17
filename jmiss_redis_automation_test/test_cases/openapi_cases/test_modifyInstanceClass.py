from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestModifyInstanceClass:


    def test_modifyInstanceClass(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_class_visibility(config, "redis.m1.micro.basic", 1, client)
        assertRespNotNone(resp)




