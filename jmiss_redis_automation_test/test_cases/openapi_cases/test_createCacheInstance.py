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

    @pytest.mark.intergration
    def test_specified_standard_createCacheInstance(self, config, instance_data):
        instances = instance_data["create_shardard_specified"]
        print("Standard instances count is %s" % len(instances))
        for i in range(len(instances)):
            client, _, instance_id = create_validate_instance(config, instances[i])

            if instance_id is not None:
                delete_instance(config, instance_id, client)

    @pytest.mark.intergration
    def test_specified_cluster_createCacheInstance(self, config, instance_data):
        instances = instance_data["create_cluster_specified"]
        print("Cluster instances count is %s" % len(instances))
        for i in range(len(instances)):
            client, _, instance_id = create_validate_instance(config, instances[i])

            if instance_id is not None:
                delete_instance(config, instance_id, client)


