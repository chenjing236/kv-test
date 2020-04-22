#!/bin/python
# coding:utf-8

import pytest
from jmiss_redis_automation_test.steps.FailoverOperation import *
from jmiss_redis_automation_test.steps.base_test.admin import *
from jmiss_redis_automation_test.steps.base_test.proxy import *
from jmiss_redis_automation_test.steps.base_test.redis import *
from jmiss_redis_automation_test.steps.base_test.configmap import *


class TestFailover:
    @pytest.mark.failover
    def test_admin_failover(self, init_instance, config):
        try:
            client, resp, instanceId = init_instance

            status = trigger_admin_failover(config, instanceId, config["region"])
            assert status == 200

            

            adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                     "paas_nvmes.n1.1C_1GB_4GB",
                                     "57 2 1 ? * 0,1,2,3,4,5,6", "")
            assert check_all_admin(instanceId, config, adminObject) == True

            proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
            assert check_all_proxy(instanceId, config, proxyObject)

            redisObject = redisParam("paas_nvmes.n1.1C_2GB_8GB", "104857600", "1048576", ["0 16383"], "volatile-lru",
                                     "", 0,
                                     "", 1)
            assert check_all_redis(instanceId, config, redisObject)

            configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
            assert check_all_configmap(instanceId, config, configObject)
        except ValueError as e:
            print ("except", e)

    # 单个proxy发生failover，原地启动
    def test_proxy_failover_local(self, init_instance, config):
        client, resp, instanceId = init_instance

        status = trigger_proxy_failover(config, instanceId, config["region"], 0)
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)

    # 单个proxy发生failover，换机器启动
    def test_proxy_failover_notLocal(self, init_instance, config):
        client, resp, instanceId = init_instance

        status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)

    # 超过一半的proxy同时发生failover
    def test_multi_proxy_failover(self, init_instance, config):
        client, resp, instanceId = init_instance

        status = trigger_proxy_failover(config, instanceId, config["region"], 0, 1)
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)

    # 单个slave发生failover，原地启动
    def test_redis_slave_failover_local(self, init_instance, config):
        client, resp, instanceId = init_instance

        current_rs_type = get_current_rs_type(instanceId, config)

        status = trigger_redis_failover(config, instanceId, config["region"],
                                        instanceId + "-slave-" + current_rs_type + "-0")
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        redisObject = redisParam("paas_nvmes.n1.1C_2GB_8GB", "104857600", "1048576", ["0 16383"], "volatile-lru",
                                 "", 0,
                                 "", 1)
        assert check_all_redis(instanceId, config, redisObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)

    # 单个slave发生failover，换机器启动
    def test_redis_slave_failover_local(self, init_instance, config):
        client, resp, instanceId = init_instance

        current_rs_type = get_current_rs_type(instanceId, config)

        status = trigger_redis_failover(config, instanceId, config["region"],
                                        instanceId + "-slave-" + current_rs_type + "-0", 1)
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        redisObject = redisParam("paas_nvmes.n1.1C_2GB_8GB", "104857600", "1048576", ["0 16383"], "volatile-lru",
                                 "", 0,
                                 "", 1)
        assert check_all_redis(instanceId, config, redisObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)

    # 多个slave发生failover
    def test_multi_redis_slave_failover(self, init_instance, config):
        client, resp, instanceId = init_instance

        current_rs_type = get_current_rs_type(instanceId, config)

        status = trigger_redis_failover(config, instanceId, config["region"],
                                        instanceId + "-slave-" + current_rs_type + "-0", 1)
        assert status == 200

        adminObject = admimParam(0, "a", "b", False, 0, "", "", "Running", 0, "Running", "",
                                 "paas_nvmes.n1.1C_1GB_4GB",
                                 "57 2 1 ? * 0,1,2,3,4,5,6", "")
        assert check_all_admin(instanceId, config, adminObject) == True

        proxyObject = proxyParam("paas_nvmes.n1.1C_1GB_4GB", 5000, 48, 0, "")
        assert check_all_proxy(instanceId, config, proxyObject)

        redisObject = redisParam("paas_nvmes.n1.1C_2GB_8GB", "104857600", "1048576", ["0 16383"],
                                 "volatile-lru",
                                 "", 0,
                                 "", 1)
        assert check_all_redis(instanceId, config, redisObject)

        configObject = configMapParam(0, "", "Running", 0, "a", "b", "", "104857600", False, "")
        assert check_all_configmap(instanceId, config, configObject)


