from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestResetCacheInstancePassword:

    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.jdstack
    def test_resetCacheInstancePassword(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_password(config, instance_id, config["change_data"]["instancePassword"], client)
        assertRespNotNone(resp)

    @pytest.mark.stability
    def test_resetCacheInstancePassword_webcli(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instance_id = create_validate_instance(config, instance, expected_object)

        resp = reset_password(config, instance_id, config["change_data"]["instancePassword"], client)

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]], config["change_data"]["instancePassword"])
        resp = send_web_command(config, instance_id, config["region"], "auth " + config["change_data"]["instancePassword"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.runAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, 1)

	if instance_id is not None:
            delete_instance(config, instance_id, client)
