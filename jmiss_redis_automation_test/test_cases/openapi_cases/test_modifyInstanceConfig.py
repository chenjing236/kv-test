from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


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

    @pytest.mark.stability
    @pytest.mark.cjtestdebug617
    def test_modifyInstanceConfig_basecheck(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instance_id = create_validate_instance(config, instance, expected_object)

        resp = set_config(config, instance_id, config["instance_config"], client)
        assertRespNotNone(resp)
        # assert by db
        query_instance_recurrent(200, 5, instance_id, config, client)
        resp = get_config(config, instance_id, client)
        assertRespNotNone(resp)
        config_list = resp.result["instanceConfig"]
        policy = {"key": "configName", "value": "configValue"}
        listCompareJason(config_list, config["instance_config"], policy)

        config_param = {"hash-max-ziplist-entries": "511", "hash-max-ziplist-value": "511", 
			"list-compress-depth": "511", "list-max-ziplist-size": "511",
                        "maxmemory-policy": "allkeys-lru", "notify-keyspace-events": "AKE",
                        "set-max-intset-entries": "511", "slowlog-log-slower-than": "511",
                        "zset-max-ziplist-entries": "511", "zset-max-ziplist-value": "511"}
        config_param_s = dict(sorted(config_param.items(),key=lambda x:x[0]))

        expected_object.config_param = config_param_s
        resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.runAllCommand()

        #assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, 1)
        if instance_id is not None:
            delete_instance(config, instance_id, client)



