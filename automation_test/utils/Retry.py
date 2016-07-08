#!/usr/bin/python
#coding:utf-8
from utils.tools import *
from utils.SQLClient import SQLClient
import time
import json

class Retry(object):
    def __init__(self,conf_obj):
        self.conf_obj = conf_obj

    def init_sql_client(self):
        return SQLClient(self.conf_obj['mysql_host'], self.conf_obj["mysql_port"], self.conf_obj["mysql_user"],self.conf_obj["mysql_passwd"],self.conf_obj["mysql_db"])

    #重试，根据space_id获取instance表中的master和sslave的记录
    def retry_get_new_container(self, space_id, container_type):
        container_ip_new = 0
        container_port_new = 0
        cur_retry_times = 0
        sql_c = self.init_sql_client()
        wait_time = self.conf_obj["wait_time"]
        retry_times = self.conf_obj["retry_times"]

        epoch_origin = sql_c.get_epoch(space_id)

        while cur_retry_times < retry_times:
            cur_retry_times = cur_retry_times + 1
            instances = sql_c.get_instances(space_id)
            epoch = sql_c.get_epoch(space_id)
            if container_type == "master":
                container_info = instances[0]
                container_ip_new = container_info[0]
                container_port_new = container_info[1]

            if container_type == "slave":
                container_info = instances[1]
                container_ip_new = container_info[0]
                container_port_new = container_info[1]

            if epoch > epoch_origin:
                print "[INFO] {0}:{1} is created by failover. Failover can recreate new {2} for cache instance (space_id={3})".format(container_ip_new,container_port_new,container_type,space_id)
                break

            is_locked = sql_c.is_locked(space_id)
            print "[INFO] Retry {0}... Failover is recreating {1} for instance (space_id={2},is_locked={3}) ...".format(cur_retry_times,container_type,space_id,is_locked)
            time.sleep(float(wait_time))

        if cur_retry_times > retry_times:
            container_ip_new = 0
            container_port_new = 0

        return container_ip_new,container_port_new