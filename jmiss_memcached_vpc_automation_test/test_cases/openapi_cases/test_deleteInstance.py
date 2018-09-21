import pytest
from jdcloud_sdk.services.memcached.apis.DeleteInstanceRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *



class TestDeleteInstance:



    # @pytest.mark.openapi
    def tes_deleteInstance(self, create_instance, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = DeleteInstanceParameters('cn-north-1',"xx")
            request = DeleteInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "------------deleteInstances--------------"
            print resp.result
        except Exception, e:
            print e


    def deleteInstance(self):
        client = setClient
        header = getHeader()
        instance_id = "mc-lb0q9yp46s"
        try:
            parameters = DeleteInstanceParameters('cn-north-1', instance_id)
            request = DeleteInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "------------deleteInstances--------------"
            print resp.result
        except Exception, e:
            print e

