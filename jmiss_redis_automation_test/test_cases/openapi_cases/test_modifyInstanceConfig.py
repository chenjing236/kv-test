from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestModifyInstanceConfig:


    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_modifyInstanceConfig(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = set_config(config, instance_id, config["instance_config"], client)
        assertRespNotNone(resp)
        #assert by db
        query_instance_recurrent(200, 5, instance_id, config, client)
        resp = get_config(config, instance_id, client)
        assertRespNotNone(resp)
        config_list = resp.result["instanceConfig"]
        policy = {"key":"configName","value":"configValue"}
        listCompareJason(config_list, config["instance_config"], policy)

