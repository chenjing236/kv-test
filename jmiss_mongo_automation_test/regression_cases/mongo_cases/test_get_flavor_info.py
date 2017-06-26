# -*- coding: utf-8 -*-

import pytest
import logging
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class TestGetFlavorInfo:
    #通过flavor信息，查看数据库flavor表中flavor id；在根据flavor id查看数据库flavor中的信息
    @pytest.mark.smoke
    def test_flavor_info(self, config, instance_data, http_client):
	# info_logger.info("[SCENARIO] Verify flavor info is the same with flavor id")
        # 获取flavor 1C_2M_4D_10E的flavor id
        info_logger.info("[STEP] Get flavor id by flavor info")
        flavor_id = get_flavorid_by_flavorinfo_step(instance_data, http_client)
        info_logger.info("[INFO] Flavor id is %s for flavor info [%s]", flavor_id, instance_data["mongo_1C_2M_4D_10E"])
        assert flavor_id != "", "[ERROR] Flavor id is none"
	# 根据flavor id获取flavor info的信息与stpe1的flavor信息一致
	flavor_info = get_flavor_info_step(instance_data, http_client, flavor_id)
	info_logger.info("[INFO] Flavor info is %s", json.dumps(flavor_info))
	assert flavor_info["cpu"] == int(instance_data["mongo_1C_2M_4D_10E"]["cpu"]), "[ERROR] CPU is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["cpu"]))
	assert flavor_info["disk"] == int(instance_data["mongo_1C_2M_4D_10E"]["disk"]), "[ERROR] Disk is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["disk"]))
	assert flavor_info["memory"] == int(instance_data["mongo_1C_2M_4D_10E"]["memory"]), "[ERROR] Memory is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["memory"]))
	assert flavor_info["iops"] == int(instance_data["mongo_1C_2M_4D_10E"]["iops"]), "[ERROR] Iops is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["iops"]))
	assert flavor_info["maxConn"] == int(instance_data["mongo_1C_2M_4D_10E"]["maxconn"]), "[ERROR] Iops is not {0}".format(int(instance_data["mongo_1C_2M_4D_10E"]["maxConn"]))
