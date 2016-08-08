import time

import pytest
from utils.redisOps import *
from utils.tools import *


class TestSetACLFunc:

    @pytest.mark.smoke
    def test_non_target(self, web_client):
        print "begin to test non-target acl"
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"ips": ips, "action": "allow"}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10  #parameter error
        assert res_data["attach"] == False
        print "test non-target acl success"

    @pytest.mark.smoke
    def test_null_target(self, web_client):
        print "begin to test null-target acl"
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(None, ips)
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        print "test null-target acl success"

    @pytest.mark.smoke
    def test_useless_spaceid(self, web_client):
        print "begin to test non-existent spaceId acl"
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl("8888", ips)
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        print "test useless spaceId acl success"

    @pytest.mark.smoke
    def test_two_spaceid(self, sql_client, web_client, created_cluster): # an useful spaceId and an useless spaceId
        print "begin to test non-existent spaceId acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": [space_id, "8888"], "ips": ips, "action": "allow"}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test non-existent spaceId acl success"


    @pytest.mark.smoke
    def test_other_spaceid(self, sql_client, web_client, created_cluster): # an useful spaceId and an useless spaceId
        print "begin to test other spaceId acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": ["8759e364-8a11-47f7-8582-fd70678867cc"], "ips": ips, "action": "allow"}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test other spaceId acl success"

    @pytest.mark.smoke
    def test_non_ips(self, sql_client, web_client, created_cluster):  # an useful spaceId and an useless spaceId
        print "begin to test non-ips acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": [space_id], "action": "allow"}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test non-ips acl success"

    @pytest.mark.smoke
    def test_null_ips(self, sql_client, web_client, created_cluster):  # an useful spaceId and an useless spaceId
        print "begin to test null-ips acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(space_id, None)
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test null-ips acl success"

    @pytest.mark.smoke
    def test_error_ips(self, sql_client, web_client, created_cluster):  # an useful spaceId and an useless spaceId
        print "begin to test error-ips acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(space_id, "192.0.0")
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test error-ips acl success"

    @pytest.mark.smoke
    def test_non_action(self, sql_client, web_client, created_cluster):  # there is no action
        print "begin to test non-action acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": [space_id]}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test non-action acl success"

    @pytest.mark.smoke
    def test_null_action(self, sql_client, web_client, created_cluster):  # the action is null
        print "begin to test null-action acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": [space_id], "action": ""}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test null-action acl success"

    @pytest.mark.smoke
    def test_error_action(self, sql_client, web_client, created_cluster):  # error action
        print "begin to test error-action acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        acl = {"target": [space_id], "action": "error"}
        status, headers, res_data = web_client.http_request("PUT", "acl", json.dumps(acl))
        print res_data
        assert status == 200
        assert res_data["code"] == -10
        assert res_data["attach"] == False
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "set acl false, it's right!"
        print "test error-action acl success"

    @pytest.mark.smoke
    def test_allow_acl(self, sql_client, web_client, created_cluster, config):
        print "begin to test allow acl"
        space_id, space_info = created_cluster
        status, capacity, password, flag, tenant_id, name, remarks = space_info
        instances = sql_client.get_instances(space_id)
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(space_id, ips)
        print res_data
        assert status == 200
        assert res_data['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips == act_ips
        print "set acl success"
        time.sleep(1)
        # check ap access
        check_ap_access(config['ap_host'], config['ap_port'], password, instances[0])
        print "test allow acl success"

    @pytest.mark.smoke
    def test_deny_acl(self, sql_client, web_client, created_cluster, config):
        print "begin to test deny acl"
        space_id, space_info = created_cluster
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.del_acl(space_id, ips)
        print res_data
        assert status == 200
        assert res_data['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        print "act_ips: ", act_ips
        assert ips != act_ips
        print "del acl success"
        time.sleep(1)
        # check ap access
        # check_ap_access(config['ap_host'], config['ap_port'], password, instances[0])
        print "test deny acl success"

