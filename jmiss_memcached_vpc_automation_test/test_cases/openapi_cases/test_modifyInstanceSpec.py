from jdcloud_sdk.services.memcached.apis.ModifyInstanceSpecRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedOperation import *



class TestModifyInstanceSpec:

    @pytest.mark.todo
    @pytest.mark.openapi
    def test_modifyInstanceSpec(self, create_instance, instance_data, config, sql_client):
        client, resp, instance_name, instance_id = create_instance
        sql_str = "select class from mc_instance where instance_id='{0}'".format(instance_id)
        header = getHeader(config)
        resp = None
        try:
            parameters = ModifyInstanceSpecParameters(config["region"], instance_id, str(instance_data["changedClass"]))
            request = ModifyInstanceSpecRequest(parameters, header)
            resp = client.send(request)
        except Exception, e:
            print e
        if resp.error is not None:
            print resp.error.code
            print resp.error.message
            assert False

        sql_client.wait_for_expectation(sql_str, str(instance_data["changedClass"]), 6, 200)
        # resp = describe(client, instance_id, config)
        # if resp is not None:
        #     assert resp.result["instance"]["instanceClass"] == instance_data["changedClass"]

