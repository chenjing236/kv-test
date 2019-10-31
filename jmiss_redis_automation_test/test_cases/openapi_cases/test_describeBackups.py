from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestDescribeBackups:

    @pytest.mark.openapi
    @pytest.mark.regression
    def test_describeBackups(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = query_backups(config, instance_id, client)
        assertRespNotNone(resp)




