import pytest
from jdcloud_sdk.services.memcached.apis.FlushInstanceRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *

class TestFlushInstance:

    @pytest.mark.openapi
    def test_flushInstance(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = FlushInstanceParameters(config["region"], instance_id)
            request = FlushInstanceRequest(parameters, header)
            resp = client.send(request)
        except Exception, e:
            print e
        assert resp is not None
        assert resp.error is None
        assert resp.result is None


    @pytest.mark.openapi
    def test_flushInstanceNotFound(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = FlushInstanceParameters(config["region"], "mc-not-found")
            request = FlushInstanceRequest(parameters, header)
            resp = client.send(request)
            checkNotFound(resp)
        except Exception, e:
            print e