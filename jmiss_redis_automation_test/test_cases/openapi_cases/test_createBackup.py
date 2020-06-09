from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestCreateBackup:

    @pytest.mark.openapi
    @pytest.mark.backup
    def test_createBackup(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)

    @pytest.mark.stability
    def test_create_Backup(self, config, instance_data, expected_data):
        instances = instance_data["create_cluster_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instance_id = create_validate_instance(config, instances[0], expected_object)

        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)

        assert check_backup(config, instance_id, str(resp.result["baseId"]), client) == True

        resp = send_web_command(config, instance_id, config["region"], "auth " + instances[0]["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.checkAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["target_shardNumber"])