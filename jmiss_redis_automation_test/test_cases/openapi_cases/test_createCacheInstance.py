from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.Valification import *



class TestCreateInstance:

    @pytest.mark.openapi
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cjdebug
    def test_createCacheInstance(self, init_instance, config,expected_data):
        client, resp, instance_id = init_instance
        assert instance_id is not None
        assertRespNotNone(resp)
        time.sleep(150)

    #@pytest.mark.intergration
    def test_specified_standard_createCacheInstance(self, config, instance_data,expected_data):
        instances = instance_data["create_standard_specified"]
        print("Standard instances count is %s" % len(instances))
        for i in range(len(instances)):
            expected_object = baseCheckPoint(expected_data[instances[i]["cacheInstanceClass"]],
                                             instances[i]["instance_password"])
            client, _, instance_id = create_validate_instance(config, instances[i],expected_object)

            if instance_id is not None:
                delete_instance(config, instance_id, client)

    @pytest.mark.intergration
    def test_specified_cluster_createCacheInstance(self, config, instance_data,expected_data):
        instances = instance_data["create_cluster_specified"]
        print("Cluster instances count is %s" % len(instances))
        for i in range(len(instances)):
            expected_object = baseCheckPoint(expected_data[instances[i]["cacheInstanceClass"]],
                                             instances[i]["instance_password"])
            client, _, instance_id = create_validate_instance(config, instances[i],expected_object)

            if instance_id is not None:
                delete_instance(config, instance_id, client)


