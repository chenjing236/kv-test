from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestCreateBackup:

    @pytest.mark.openapi
    @pytest.mark.backup
    @pytest.mark.regression
    @pytest.mark.jdstack
    def test_createBackup(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)

    @pytest.mark.stability
    def test_create_Backup(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]
        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instance_id = create_validate_instance(config, instance, expected_object)

        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)

        assert check_backup(config, instance_id, str(resp.result["baseId"]), client) == True
        baseId = str(resp.result["baseId"])
        expected_object.backup_list = [baseId]
        resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.runAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, 1)

        if instance_id is not None:
            delete_instance(config, instance_id, client)
