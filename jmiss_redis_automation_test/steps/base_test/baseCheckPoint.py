#!/bin/python
# coding:utf-8
from jmiss_redis_automation_test.utils.util import get_sha256_pwd


class baseCheckPoint():
    def __init__(self,expected_data,password):
        self.side=expected_data["side"]
        self.current_rs_type = expected_data["current_rs_type"]
        self.next_rs_type = expected_data["next_rs_type"]
        self.is_first_start = expected_data["is_first_start"]
        self.topo = expected_data["topo"]
        self.password = get_sha256_pwd(password)
        self.max_memory = expected_data["max_memory"]
        self.space_status = expected_data["space_status"]
        self.failovering_num = expected_data["failovering_num"]
        self.shard_status = expected_data["shard_status"]
        self.config_param = expected_data["config_param"]
        self.admin_flavor = expected_data["admin_flavor"]
        self.auto_backup_timer = expected_data["auto_backup_timer"]
        self.backup_list = expected_data["backup_list"]
        self.proxy_flavor = expected_data["proxy_flavor"]
        self.max_connection = expected_data["max_connection"]
        self.flow_control = expected_data["flow_control"]
        self.redis_flavor = expected_data["redis_flavor"]
        self.maxmemory_policy = expected_data["maxmemory_policy"]
        self.master_slaves = expected_data["master_slaves"]
        self.master_aof_enabled = expected_data["master_aof_enabled"]
        self.slave_master = expected_data["slave_master"]
        self.slave_aof_enabled = expected_data["slave_aof_enabled"]
