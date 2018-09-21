from jdcloud_sdk.services.memcached.apis.ModifyInstanceRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *



class TestModifyInstance:


    @pytest.mark.openapi
    def test_modifyInstances(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = ModifyInstanceParameters(config["region"], instance_id)
            parameters.setInstanceName(config["changed_data"]["instanceName"])
            parameters.setInstanceDescription(config["changed_data"]["instanceDescription"])
            # parameters.setMcAuth(True)
            # parameters.setMcPswd()
            request = ModifyInstanceRequest(parameters, header)
            resp = client.send(request)
        except Exception, e:
            print e

        assert resp.error is not None
        resp = describe(self, create_instance, config)
        if resp.result is not None:
            validateResult(resp.result, instance_data.changed_data)
        else:
            assert False


