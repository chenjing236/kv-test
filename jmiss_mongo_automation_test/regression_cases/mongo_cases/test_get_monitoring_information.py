# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestGetMonitoringInformation:
    # 获取mongo实时信息
    @pytest.mark.smoke
    def test_get_real_time_info(self, config, instance_data, http_client, create_mongo_instance):
        info_logger.info("[SCENARIO] Get real time info of the mongo instance")
        # 创建mongo实例
        info_logger.info("[STEP] Create a mongo instance")
        space_id = create_mongo_instance
        if None == space_id:
                assert False, "[ERROR] It is failed to create mongo instance"
        info_logger.info("[INFO] The mongo instance %s is created", space_id)
        # 通过接口获取实时信息
        info_logger.info("[STEP] Get the real time info")
        real_time_info=get_real_time_info_step(config, instance_data, http_client, space_id)
        if None != real_time_info:
                info_logger.info("[INFO] The real time info for the mongo instance is %s", json.dumps(real_time_info))
        else:
                info_logger.info("[INFO] The real time info for the mongo instance is %s", real_time_info)
        # 验证接口返回"成功"
        assert "成功".decode() in real_time_info or real_time_info is not None, "[ERROR] The interface for the real time info cannot work"

    # 获取mongo实例的监控信息
    @pytest.mark.smoke
    def test_get_monitor_message(self, config, instance_data, http_client, create_mongo_instance):
        info_logger.info("[SCENARIO] Get the monitor message of the mongo instance")
        # 创建mongo实例
        info_logger.info("[STEP] Create a mongo instance")
        space_id = create_mongo_instance
        if None == space_id:
                assert False, "[ERROR] It is failed to create mongo instance"
        info_logger.info("[INFO] The mongo instance %s is created", space_id)
        # 通过接口获取监控信息
        message, monitor_info = get_monitor_info_step(config, instance_data, http_client, space_id)
        # 验证接口返回的值可以显示
        if None != monitor_info:
                info_logger.info("[INFO] The result of getting monitoring message is %s, and the monitor message is %s", message, json.dumps(monitor_info))
        else:
                info_logger.info("[INFO] The result of getting monitoring message is %s, and the monitor message is %s", message, monitor_info)
        assert "成功".decode() in message, "[ERROR] Cannot get the monitor message"
