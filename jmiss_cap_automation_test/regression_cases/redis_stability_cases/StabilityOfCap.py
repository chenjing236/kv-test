# -*- coding: utf-8 -*-

from BasicTestCase import *
from redis_stability_cases.ClearRemindedRedis import clear_reminded_redis

logger_info = logging.getLogger(__name__)

class TestCreateRedis:
    # =====fixtures========

    def setup(self):
        print ("setup----->")

    def teardown(self):
        print ("teardown-->")

    def setup_class(cls):
        print ("\n")
        print ("setup_class=========>")

    def teardown_class(cls):
        print ("teardown_class=========>")

    def setup_method(self, method):
        print ("setup_method----->>")

    def teardown_method(self, method):
        print ("teardown_method-->>")

    def test_create_redis(self):




