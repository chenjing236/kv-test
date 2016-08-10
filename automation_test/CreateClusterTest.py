# coding=utf-8
import pytest
from utils.WebClient import *


class TestCreateClusterFunc:

    # 超过200个英文字符，201个字符
    @pytest.mark.smoke
    def test_more_than_200_EngName(self, sql_client, web_client):
        print "[test] begin to test create cluster with a more than 200 characters English name"
        longName = "test_create_cluster_with_an_English_name_more_than_two_hundred_characters_" \
                   "test_create_cluster_with_an_English_name_more_than_two_hundred_characters_" \
                   "test_create_cluster_with_an_English_name_more_than_tw"
        ca = CreateArgs(2097152, 1, "create_test", longName, 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster with a more than 200 characters English name success!"

    # 超过100字符的中文名称，101个文字
    @pytest.mark.smoke
    def test_more_than_100_ChnName(self, sql_client, web_client):
        print "[test] begin to test create cluster with a more than 100 characters Chinese name"
        longName = "测试创建超过一百个文字的中文名称的缓存实例" \
                   "测试创建超过一百个文字的中文名称的缓存实例" \
                   "测试创建超过一百个文字的中文名称的缓存实例" \
                   "测试创建超过一百个文字的中文名称的缓存实例" \
                   "测试创建超过一百个文字的中文名称的"  # 101个文字
        ca = CreateArgs(2097152, 1, "create_test", longName, 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster with a more than 100 characters Chinese name success!"

    # @pytest.mark.smoke
    # def test_less_than_100_ChnName(self, sql_client, web_client):
    #     print "[test] begin to test create cluster with a more than 100 characters Chinese name"
    #     chnName = u"测试小于一百个文字的名称"
    #     ca = CreateArgs(2097152, 1, "create_test", chnName, 1, 1)
    #     data = ca.to_json_string()
    #     status, headers, res_data = web_client.http_request("POST", "clusters", data)
    #     space_id = res_data['attach']
    #     print "res_data: ", res_data
    #     assert status == 200
    #     assert res_data['code'] == 1
    #     # check space name
    #     status, headers, res_data = web_client.get_cluster(space_id)
    #     assert status == 200
    #     assert res_data['code'] == 1
    #     cluster = res_data["attach"]
    #     assert cluster["name"] == chnName
    #     print "space_name is right"
    #     # del cluster
    #     print "test create cluster with a less than 100 characters Chinese name success!"

    @pytest.mark.smoke
    def test_null_space_type(self, web_client):
        print "[test] begin to test create cluster with null space type"
        ca = CreateArgs(2097152, 1, "create_test", "create_cluster", None, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster with null space type success!"

    @pytest.mark.smoke
    def test_2_space_type(self, web_client):
        print "[test] begin to test create cluster when space type = 2"
        ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 2, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster when space type = 2 success!"

    @pytest.mark.smoke
    def test_null_capacity(self, web_client):
        print "[test] begin to test create cluster when capacity = null"
        ca = CreateArgs(None, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster when capacity = null success!"

    @pytest.mark.smoke
    def test_0_capacity(self, web_client):
        print "[test] begin to test create cluster when capacity = 0"
        ca = CreateArgs(0, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster when capacity = 0 success!"

    @pytest.mark.smoke
    def test_512k_capacity(self, web_client):
        print "[test] begin to test create cluster when capacity = 524288(512k)"
        ca = CreateArgs(524288, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster when capacity = 524288(512k) success!"

    @pytest.mark.smoke
    def test_2G1B_capacity(self, web_client):
        print "[test] begin to test create cluster when capacity = 2097153(2G+1byte)"
        ca = CreateArgs(2097153, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['code'] == -10
        assert res_data["msg"] == u"参数错误"
        print "test create cluster when capacity = 2097153(2G+1byte) success!"

    @pytest.mark.smoke
    def test_null_version(self, web_client):
        print "[test] begin to test create cluster when version = null"
        ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data, None)
        print "res_data: ", res_data
        assert status == 200
        assert res_data['Code'] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test create cluster when version = null success!"

    @pytest.mark.smoke
    def test_v2_version(self, web_client):
        print "[test] begin to test create cluster when version = v2.0"
        ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 1, 1)
        data = ca.to_json_string()
        status, headers, res_data = web_client.http_request("POST", "clusters", data, "v2.0")
        print "res_data: ", res_data
        assert status == 200
        assert res_data['Code'] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test create cluster when version = v2.0 success!"

