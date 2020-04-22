from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestCreateInstance:

    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cjdebug
    def test_createCacheInstance(self, init_instance, config):
        client, resp, instance_id = init_instance
        assert instance_id is not None
        assertRespNotNone(resp)
        time.sleep(150)

    @pytest.mark.openapi
    @pytest.mark.intergration
    @pytest.mark.regression
    def test_specified_createCacheInstance(self, config, instance_data):
        instances = instance_data["create_specified"]
        for i in range(len(instances)):
            client, resp, instance_id = create_instance(config, instances[i])
            instance = None
            if resp.error is None and instance_id is not None:
                instance = query_instance_recurrent(200, 5, instance_id, config, client)
                config["request_id"] = resp.request_id
            else:
                config["request_id"] = ""

            assert instance_id is not None
            assertRespNotNone(resp)
            time.sleep(150)

            if instance_id is not None:
                delete_instance(config, instance_id, client)



