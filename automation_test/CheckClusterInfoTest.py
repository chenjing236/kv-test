import time

import pytest
from utils.redisOps import *
from utils.tools import *
from utils.WebClient import *


class TestCheckClusterFunc:
    def compare_instance(self, jinstance, jinstance_expect, space_id):
        ip, port, copy_id, flag = jinstance_expect
        assert jinstance['ip'] == ip
        assert jinstance['port'] == port
        assert jinstance['copyId'] == copy_id
        assert jinstance['flag'] == flag
        assert jinstance['spaceId'] == space_id

    def check_cluster_info(self, cluster, space, instances, space_id, domian):
        status, capacity, password, flag, tenant_id, name, remarks = space
        assert cluster['status'] == status
        assert cluster['flag'] == flag
        assert cluster['capacity'] == capacity
        assert cluster['password'] == password
        assert cluster['tenantId'] == tenant_id
        assert cluster['name'] == name
        assert cluster['remarks'] == remarks
        assert cluster['spaceId'] == space_id
        assert cluster['domain'] == domian
        jinstance = cluster['instances']
        assert len(jinstance) == 2
        if jinstance[0]['copyId'] != 'm':
            tmp = jinstance[0]
            jinstance[0] = jinstance[1]
            jinstance[1] = tmp
        self.compare_instance(jinstance[0], instances[0], space_id)
        self.compare_instance(jinstance[1], instances[1], space_id)

    @pytest.mark.smoke
    def test_get_cluster(self, sql_client, web_client, created_cluster):
        # wc = WebClient(conf_obj["host"], conf_obj["pin"], conf_obj["auth_token"])
        space_id, space_info = created_cluster
        instances = sql_client.get_instances(space_id)
        assert instances is not None
        check_redis_instances(instances)
        print "check cluster success"

        # test get cluster
        status, headers, res_data = web_client.get_cluster(space_id)
        assert status == 200
        assert res_data['code'] == 1
        domain = sql_client.get_domain(space_id)
        self.check_cluster_info(res_data['attach'], space_info, instances, space_id, domain)
        print "test get cluster success"

    @pytest.mark.smoke
    def test_get_other_cluster(self, created_cluster):
        space_id, space_info = created_cluster
        web_client = WebClient("192.168.177.89", "64c8ddb08ad83c7b04fba541c3b085fd", "K1AwANjwaBmIWZBBHadr6oLC3AEIAkAtqhAJofH+ZZw=")
        status, headers, res_data = web_client.get_cluster(space_id)
        # print "get cluster response success"
        print res_data
        assert status == 200
        assert res_data['code'] == 1
        assert res_data['attach'] == None
        print "test get others' cluster success"

    @pytest.mark.smoke
    def test_non_exist_cluster(self, web_client, created_cluster):
        space_id, space_info = created_cluster
        status, headers, res_data = web_client.get_cluster(space_id + "error")
        # print "get cluster response success"
        print res_data
        assert status == 200
        assert res_data['code'] == 1
        assert res_data['attach'] == None
        print "test get non-existent cluster success"