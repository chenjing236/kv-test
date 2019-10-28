import pytest
from jdcloud_sdk.services.memcached.apis.DescribeInstancesRequest import *
from jdcloud_sdk.services.common.models.Sort import *
from jdcloud_sdk.services.common.models.Filter import Filter
from jmiss_memcached_vpc_automation_test.steps.MemcachedOperation import *



class TestDescribeInstances:

    @pytest.mark.openapi
    def test_describeInstances(self, create_instance, instance_data, config):
        client, resp, instance_name, instance_id = create_instance

        header = getHeader(config)
        try:
            parameters = DescribeInstancesParameters(config["region"])
            # parameters.setPageNumber(2)
            # parameters.setPageSize(11)
            filter1 = Filter('instanceName', 'auto_test_', 'eq')
            filter2 = Filter('instanceStatus', 'running')
            sort = Sort('createTime', 'desc')
            parameters.setSorts([sort])
            parameters.setFilters([filter1, filter2])
            request = DescribeInstancesRequest(parameters, header)
            resp = client.send(request)

        except Exception, e:
            print e

        isExist = False
        for i in resp.result['instances']:
            print i['instanceId']
            if i['instanceId'] == instance_id and i['instanceStatus'] == "running":
                isExist = True
                break
        assert isExist



