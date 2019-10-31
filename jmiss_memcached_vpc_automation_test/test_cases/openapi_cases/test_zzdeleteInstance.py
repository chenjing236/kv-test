import pytest
from jdcloud_sdk.services.memcached.apis.DeleteInstanceRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedOperation import *



class TestDeleteInstance:

    @pytest.mark.smoke
    @pytest.mark.openapi
    @pytest.mark.regression
    def test_deleteInstance(self, create_instance, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = DeleteInstanceParameters(config["region"], instance_id)
            request = DeleteInstanceRequest(parameters, header)
            time.sleep(150)
            resp = client.send(request)
            if resp.error is not None:
                assert False
        except Exception, e:
            print e


