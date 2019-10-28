from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeBackupPolicy:

    @pytest.mark.openapi
    def test_describeBackupPolicy(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_backup_policy(config, instance_id, client)
        assertRespNotNone(resp)




