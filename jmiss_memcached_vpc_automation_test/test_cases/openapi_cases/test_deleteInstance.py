import pytest
from jdcloud_sdk.services.memcached.apis.DeleteInstanceRequest import *
from steps.MemcachedClient import *



class TestDeleteInstance:



    # @pytest.mark.openapi
    def auto_deleteInstance(self, create_instance, config):
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


