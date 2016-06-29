#!/usr/bin/python
#coding:utf-8
from utils.tools import *
from utils.SQLClient import SQLClient
import time
import json

class Retry(object):
    def __init__(self,conf_path):
        self.conf_obj = json.load(open(conf_path, 'r'))
        self.container_daemon = self.conf_obj['docker_daemon']

    def init_sql_client(self):
        return SQLClient(self.conf_obj['mysql_host'], self.conf_obj["mysql_port"], self.conf_obj["mysql_user"],self.conf_obj["mysql_passwd"],self.conf_obj["mysql_db"])

    #重试，根据space_id获取instance表中的slave的记录
    def retry_get_new_slave(self,space_id,slave_ip,slave_port):
        '''
            :param space_id,slave_ip,slave_port:
            :return: [slave_port_new]
        '''
        slave_ip_new = 0
        slave_port_new = 0
        sql_c = self.init_sql_client()
        while True:
            slave_info = sql_c.get_slave_ip_port(space_id)
            slave_ip_new = slave_info[0]
            slave_port_new = slave_info[1]
            if (slave_port_new != 0) and (slave_ip_new != 0) and (not ((slave_ip == slave_ip_new) and (slave_port ==  slave_port_new))):
                print "[INFO] {0}:{1} is created by failover. Failover can recreate new slave for cache instance (space_id={2})".format(slave_ip_new,slave_port_new,space_id)
                break
            is_locked = sql_c.is_locked(space_id)
            print "[INFO] Failover is recreating slave for instance (space_id={0},is_locked={1}) ...".format(space_id,is_locked)
            time.sleep(5)

        return slave_port_new

    #重试，根据space_id获取instance表中的master的记录
    def retry_get_new_master(self,space_id,master_ip,master_port):
        '''
            :param space_id,master_ip,master_port:
            :return: [master_port_new]
        '''
        master_ip_new = 0
        master_port_new = 0
        sql_c = self.init_sql_client()
        while True:
            master_info = sql_c.get_master_ip_port(space_id)
            master_ip_new = master_info[0]
            master_port_new = master_info[1]
            if (master_port_new != 0) and (master_ip_new != 0) and (not ((master_ip == master_ip_new) and (master_port ==  master_port_new))):
                print "[INFO] {0}:{1} is created by failover. Failover can recreate new master for cache instance (space_id={2})".format(master_ip_new,master_port_new,space_id)
                break
            is_locked = sql_c.is_locked(space_id)
            print "[INFO] Failover is recreating master for instance (space_id={0},is_locked={1}) ...".format(space_id,is_locked)
            time.sleep(5)

        return master_port_new