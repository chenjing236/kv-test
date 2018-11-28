from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestCreateBackup:

    @pytest.mark.openapi
    def test_createBackup(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)




