import pytest
from jdcloud_sdk.services.memcached.apis.CreateInstanceRequest import *
from jdcloud_sdk.services.memcached.models.InstanceSpec import *
from jdcloud_sdk.services.charge.models.ChargeSpec import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *



class TestCreateInstance:

    @pytest.mark.openapi
    def test_createInstanceWithPassword(self, create_instance, config):
        client, resp, instance_name, instance_id = create_instance
        assert resp.error is None
        assert instance_id is not None


    @pytest.mark.openapi
    def test_createInstanceWithoutPassword(self, config):
        client = setClient(config)
        header = getHeader(config)
        name = "auto_test_" + str(int(time.time()))
        try:
            charge = ChargeSpec('postpaid_by_duration', 'year', 1)
            instance = InstanceSpec('MC-S-1C1G', 'single', config["az"],
                                    config["vpc"], config["subnet"], name,
                                    config["version"], False, charge, "desc")
            parameters = CreateInstanceParameters(config["region"], instance)
            request = CreateInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                assert False
        except Exception, e:
            print e
        instance = query_instance_recurrent(100, 6, name, config)


