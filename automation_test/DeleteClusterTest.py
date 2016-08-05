# coding=utf-8
import pytest
from utils.redisOps import *
from utils.tools import *
from utils.JCacheUtils import *
from utils.WebClient import *
import requests


class TestCreateClusterFunc:

    @pytest.mark.smoke
    def test_non_spaceId(self, web_client):
        print "[test] begin to test delete cluster without spaceId"
        status, headers, res_data = web_client.http_request("DELETE", "clusters")
        print "res_data: ", res_data
        assert status == 200
        assert res_data['Code'] == "-20"
        print "test delete cluster without spaceId success!"

    @pytest.mark.smoke
    def test_error_spaceId(self, web_client):
        print "[test] begin to test delete cluster with error spaceId"
        status, headers, res_data = web_client.http_request("DELETE", "clusters/{0}".format("error"))
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -50
        assert res_data['msg'] == u"spaceId不存在"
        print "test delete cluster with error spaceId success!"

    @pytest.mark.smoke
    def test_other_spaceId(self, web_client):
        print "[test] begin to test delete cluster with others' spaceId"
        status, headers, res_data = web_client.http_request("DELETE", "clusters/{0}".format("8759e364-8a11-47f7-8582-fd70678867cc"))
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -50
        assert res_data['msg'] == u"spaceId不存在"
        print "test delete cluster with others' spaceId success!"

    @pytest.mark.smoke
    def test_acl_after_delete(self, sql_client, web_client, config):
        ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 1, 1)
        space_id, space_info = CreateCluster(web_client, ca, sql_client)
        status, capacity, passwd, flag, tenant_id, name, remarks = space_info
        instances = sql_client.get_instances(space_id)
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(space_id, ips)
        assert status == 200
        assert res_data['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        assert ips == act_ips
        print "set acl success"
        # del cluster
        DeleteCluster(web_client, space_id, sql_client)
        # check ap access
        cnt = redis.StrictRedis(host=config["ap_host"], port=config["ap_port"], password=passwd)
        try:
            cnt.set("test_ap", "test_ap_value")
        except OSError:
        # except requests.exceptions.ConnectionError:
            pass

        cnt.set("test_ap", "test_ap_value")
        assert cnt.get("test_ap") == "test_ap_value"

        cnt_ins = redis.StrictRedis(host=instances[0][0], port=instances[0][1])
        assert cnt_ins.get("test_ap") == "test_ap_value"
