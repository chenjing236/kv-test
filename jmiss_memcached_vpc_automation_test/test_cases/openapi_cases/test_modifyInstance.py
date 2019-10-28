from jdcloud_sdk.services.memcached.apis.ModifyInstanceRequest import *
from jmiss_memcached_vpc_automation_test.steps.MemcachedOperation import *



class TestModifyInstance:


    @pytest.mark.openapi
    def test_modifyInstance(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance
        header = getHeader(config)
        try:
            parameters = ModifyInstanceParameters(config["region"], instance_id)
            parameters.setInstanceName(str(instance_data["changed_data"]["instanceName"]))
            parameters.setInstanceDescription(str(instance_data["changed_data"]["instanceDescription"]))
            request = ModifyInstanceRequest(parameters, header)
            resp = client.send(request)
        except Exception, e:
            print e

        assert resp.error is None
        response = describe(client, instance_id, config)
        if response.result is not None:
            validateResult(response.result["instance"], instance_data["changed_data"])
        else:
            assert False

    @pytest.mark.openapi
    def test_modifyInstanceWithoutAuth(self, create_instance, instance_data, config, sql_client):
        client, resp, instance_name, instance_id = create_instance
        sql_str = "select auth from mc_instance where instance_id='{0}'".format(instance_id)
        header = getHeader(config)
        try:
            parameters = ModifyInstanceParameters(config["region"], instance_id)
            parameters.setMcAuth(False)
            request = ModifyInstanceRequest(parameters, header)
            resp = client.send(request)
        except Exception, e:
            print e

        assert resp.error is None
        result = sql_client.exec_query_one(sql_str)
        assert result[0] == 0
