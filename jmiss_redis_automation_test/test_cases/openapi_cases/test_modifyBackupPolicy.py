from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestModifyBackupPolicy:

    @pytest.mark.openapi
    @pytest.mark.regression
    @pytest.mark.jdstack
    def test_modifyBackupPolicy(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = reset_backup_policy(config, instance_id, client)
        assertRespNotNone(resp)




