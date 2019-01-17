from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestRestoreInstance:

    @pytest.mark.todo
    def test_restoreInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)
        if resp.result["baseId"] is not None:
            base_Id = resp.result["baseId"]
            resp = restore_instance(config, instance_id, base_Id, client)
            assertRespNotNone(resp)
        else:
            assert False




