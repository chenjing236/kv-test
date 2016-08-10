# coding=utf-8
import time
import httplib
import pytest
from utils.redisOps import *
from utils.WebClient import *
from utils.tools import *


class TestCommonFunc:

    @pytest.mark.smoke
    def test_none_token(self, config):
        print "[test]begin to test request without token"
        hc = httplib.HTTPConnection(config["host"])
        # without token
        hc.request("GET", "/{0}/{1}/{2}".format("v1.0", config["pin"], "clusters/"), None, {})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request without token success"

    @pytest.mark.smoke
    def test_null_token(self, config):
        print "[test]begin to test request with null token"
        web_client = WebClient(config["host"], config["pin"], None)
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request with null token success"

    @pytest.mark.smoke
    def test_error_token(self, config):
        print "[test]begin to test request with error token"
        web_client = WebClient(config["host"], config["pin"], config["auth_token"] + "error")
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request with error token success"

    @pytest.mark.smoke
    def test_none_pin(self, config):
        print "[test]begin to test request without md5_pin"
        hc = httplib.HTTPConnection(config["host"])
        # without pin
        hc.request("GET", "/{0}/{1}".format("v1.0", "clusters/"), None, {"auth-Token": config["auth_token"]})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request without md5_pin success"

    @pytest.mark.smoke
    def test_null_pin(self, config):
        print "[test]begin to test request with null md5_pin"
        web_client = WebClient(config["host"], None, config["auth_token"])
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request with null md5_pin success"

    @pytest.mark.smoke
    def test_error_pin(self, config):
        print "[test]begin to test request with error md5_pin"
        web_client = WebClient(config["host"], config["pin"] + "error", config["auth_token"])
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request with error md5_pin success"

    # right pin and token, but do not match
    @pytest.mark.smoke
    def test_notmatch_token(self, config):
        print "[test]begin to test request pin and token do not match"
        self.auth_token = "K1AwANjwaBmIWZBBHadr6oLC3AEIAkAtqhAJofH+ZZw="
        web_client = WebClient(config["host"], config["pin"], self.auth_token)
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        assert res_data["Msg"] == u"非法请求"
        print "test request pin and token do not match success"