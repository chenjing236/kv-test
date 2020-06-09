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


    @pytest.mark.config
    def test_modify_instance_config(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instance_id = create_validate_instance(config, instances[0], expected_object)

        configs={"maxmemory-policy":"allkeys-lfu"}

        resp = set_config(config, instance_id, configs, client)
        assertRespNotNone(resp)
        expected_object.maxmemory_policy="allkeys-lfu"
        expected_object.config_param="{\"maxmemory-policy\":\"allkeys-lfu\"}"

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["shardNumber"])

    @pytest.mark.stability
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

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],
                                         instance["instance_password"])

        resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.checkAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["target_shardNumber"])

