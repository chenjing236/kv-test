from jmiss_redis_automation_test.steps.BackupOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.steps.WebCommand import *


class TestRestoreInstance:

    @pytest.mark.openapi
    @pytest.mark.regression
    @pytest.mark.jdstack
    def test_restoreInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        resp = create_backup(config, instance_id, client)
        assertRespNotNone(resp)
        if resp.result["baseId"] is not None:
            base_Id = resp.result["baseId"]
            time.sleep(150)
            side = get_current_rs_type(instance_id, config)
            print "--- restore_instance ---"
            resp = restore_instance(config, instance_id, base_Id, client)
            assertRespNotNone(resp)
            print "--- wait for restore finished ---"
            for i in range(0, 1200):
                redisNum = get_redis_num(instance_id, config, str(side))
                print("%d redisNum is %s" % (i, redisNum))
                if redisNum == 0:
                    print ("restore successd")
                    break
                sleep(1)
        else:
            assert False

    @pytest.mark.restoredata
    def test_restoreInstance_data(self, init_instance, config):
        client, resp, instance_id = init_instance

        # sleep(10)
        print "--- write data ---"
        resp = send_web_command(config, instance_id, config["region"],
                                "auth " + config["change_data"]["instancePassword"])
        token = resp.result["token"]
        object = WebCommand(config, instance_id, config["region"], token)
        object.runSetCommand(100)

        object.command = "dbsize"
        oldDbNum = object.runCommand()

        resp = create_backup(config, instance_id, client)
        # assertRespNotNone(resp)
        if resp.result["baseId"] is not None:
            base_Id = resp.result["baseId"]
            time.sleep(150)
            side = get_current_rs_type(instance_id, config)
            print "--- restore_instance ---"
            resp = restore_instance(config, instance_id, base_Id, client)
            assertRespNotNone(resp)
            print "--- wait for restore finished ---"
            for i in range(0, 1200):
                redisNum = get_redis_num(instance_id, config, str(side))
                print("%d redisNum is %s" % (i, redisNum))
                if redisNum == 0:
                    print ("restore successd")
                    break
                sleep(1)

            resp = send_web_command(config, instance_id, config["region"],
                                    "auth " + config["change_data"]["instancePassword"])
            token = resp.result["token"]
            object.token = token
            newDbNum = object.runCommand()
            assert oldDbNum == newDbNum
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
        assert check_backup(config, instance_id, base_Id, client) is True

        resp = restore_instance(config, instance_id, base_Id, client)
        assertRespNotNone(resp)

        expected_object.side = 1
        expected_object.current_rs_type = "b"
        expected_object.next_rs_type = "a"
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
        # object.checkAllCommand()

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["shardNumber"])

        if instance_id is not None:
            delete_instance(config, instance_id, client)
