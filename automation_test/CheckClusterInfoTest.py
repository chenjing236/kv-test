import time

import pytest
from utils.redisOps import *
from utils.tools import *
from utils.WebClient import *
from utils.JCacheUtils import *


class TestCheckClusterFunc:

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
        CheckClusterInfo(res_data['attach'], space_info, instances, space_id, domain)
        print "test get cluster success"

    @pytest.mark.smoke
    def test_get_other_cluster(self, created_cluster, config):
        other_pin = "64c8ddb08ad83c7b04fba541c3b085fd"
        other_token = "K1AwANjwaBmIWZBBHadr6oLC3AEIAkAtqhAJofH+ZZw="
        space_id, space_info = created_cluster
        web_client = WebClient(config["host"], other_pin, other_token )
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