from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestRestoreInstance:

    @pytest.mark.openapi
    @pytest.mark.regression
    def test_restoreInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)
        if resp.result["baseId"] is not None:
            base_Id = resp.result["baseId"]
            time.sleep(150)
            resp = restore_instance(config, instance_id, base_Id, client)
            assertRespNotNone(resp)
        else:
            assert False

    @pytest.mark.restore
    @pytest.mark.stability
    def test_restore(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instance_id = create_validate_instance(config, instances[0], expected_object)
        old_current_rs_type = expected_object.current_rs_type

        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)

        base_Id = str(resp.result["baseId"])
        assert check_backup(config, instance_id, base_Id, client) == True

        resp = restore_instance(config, instance_id, base_Id, client)
        assertRespNotNone(resp)

        expected_object.side = 1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"
        expected_object.backup_list.append(base_Id)

        for i in range(0, 1200):
            redisNum = get_redis_num(instance_id, config, old_current_rs_type)
            if redisNum == 0:
                print ("restore successd")
                break
            sleep(1)

        query_instance_recurrent(200, 5, instance_id, config, client)
        resp = send_web_command(config, instance_id, config["region"], "auth " + instances[0]["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.checkAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["shardNumber"])










