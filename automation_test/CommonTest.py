# coding="utf-8"
import time
import httplib
import pytest
from utils.redisOps import *
from utils.WebClient import *
from utils.tools import *


class TestCommonFunc:

    @pytest.mark.smoke
    def test_without_token(self, config):
        web_client = WebClient(config["host"], config["pin"], None)
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        print "test request without token success"

    @pytest.mark.smoke
    def test_error_token(self, config):
        web_client = WebClient(config["host"], config["pin"], config["auth_token"] + "error")
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        print "test request with error token success"

    @pytest.mark.smoke
    def test_without_pin(self, config):
        web_client = WebClient(config["host"], None, config["auth_token"])
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        print "test request without md5_pin success"

    @pytest.mark.smoke
    def test_error_pin(self, config):
        web_client = WebClient(config["host"], config["pin"] + "error", config["auth_token"])
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        print "test request with error md5_pin success"

    # right pin and token, but do not match
    @pytest.mark.smoke
    def test_notmatch_token(self, config):
        self.auth_token = "K1AwANjwaBmIWZBBHadr6oLC3AEIAkAtqhAJofH+ZZw="
        web_client = WebClient(config["host"], config["pin"], self.auth_token)
        status, headers, res_data = web_client.get_clusters()
        print res_data
        assert res_data["Code"] == "-20"
        print "test request pin and token do not match success"