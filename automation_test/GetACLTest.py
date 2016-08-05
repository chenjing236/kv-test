import pytest
from utils.redisOps import *
from utils.tools import *


class TestGetACLFunc:

    @pytest.mark.smoke
    def test_non_spaceId(self, web_client, config):
        print "[test]begin to test non-spaceId get acl"
        # get acl
        status, headers, res_data = web_client.http_request("GET", "acl")
        print res_data
        assert status == 200
        assert res_data["Code"] == "-20"
        print "test non-spaceId get acl success"

    @pytest.mark.smoke
    def test_error_spaceId(self, web_client, config):
        print "[test]begin to test error-spaceId get acl"
        # get acl
        status, headers, res_data = web_client.get_acl("error") # error spaceId
        print res_data
        assert status == 200
        assert res_data["code"] == -50
        assert res_data["attach"] == None
        print "test error-spaceId get acl success"

    @pytest.mark.smoke
    def test_non_acl(self, sql_client, web_client, created_cluster, config):
        print "[test]begin to test non_acl get acl"
        space_id, space_info = created_cluster
        # get acl
        status, headers, res_data = web_client.get_acl(space_id)  # right spaceId
        print res_data
        assert status == 200
        assert res_data["code"] == 1
        assert res_data["attach"] == {'ips': None}
        print "test non_acl get acl success"

    @pytest.mark.smoke
    def test_right_acl(self, sql_client, web_client, created_cluster, config):
        print "[test]begin to test right_acl get acl"
        space_id, space_info = created_cluster
        # set acl
        local_ip = get_local_ip()
        ips = [local_ip]
        web_client.set_acl(space_id, ips)
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips == act_ips
        print "set acl success"
        # get acl
        status, headers, res_data = web_client.get_acl(space_id)  # right spaceId
        print "get acl success: ", res_data
        assert status == 200
        assert res_data["code"] == 1
        assert res_data["attach"] == {'ips': ips}
        # del acl
        status1, headers1, res_data1 = web_client.del_acl(space_id, ips)
        print res_data1
        assert status1 == 200
        assert res_data1['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "del acl success"
        print "test right_acl get acl success"

    @pytest.mark.smoke
    def test_del_acl(self, sql_client, web_client, created_cluster, config):
        print "[test]begin to test del_acl get acl"
        space_id, space_info = created_cluster
        # set acl
        local_ip = get_local_ip()
        ips = [local_ip]
        web_client.set_acl(space_id, ips)
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips == act_ips
        print "set acl success"
        # del acl
        status1, headers1, res_data1 = web_client.del_acl(space_id, ips)
        print res_data1
        assert status1 == 200
        assert res_data1['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "del acl success"
        # get acl
        status, headers, res_data = web_client.get_acl(space_id)  # right spaceId
        print "get acl success: ", res_data
        assert status == 200
        assert res_data["code"] == 1
        assert res_data["attach"] == {'ips': None}
        print "test del_acl get acl success"
