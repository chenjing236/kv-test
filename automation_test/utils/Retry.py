#!/usr/bin/python
#coding:utf-8
from utils.tools import *
from utils.SQLClient import SQLClient
import time
import json

#获取conf.json的绝对路径
conf_path = cur_file_dir() + "\conf.json"
conf_obj = json.load(open(conf_path, 'r'))
#Docker守护进程的port
container_daemon = conf_obj['docker_daemon']

def init():
    return SQLClient(conf_obj['mysql_host'], conf_obj["mysql_port"], conf_obj["mysql_user"],conf_obj["mysql_passwd"],conf_obj["mysql_db"])

def retry_get_new_slave(space_id,slave_port):
    slave_ip_new = 0
    slave_port_new = 0
    sql_c = init()
    while 1==1:
        slave_info = sql_c.get_slave_ip_port(space_id)
        slave_ip_new = slave_info[0]
        slave_port_new = slave_info[1]
        if (slave_port_new != slave_port) and (slave_port_new != 0) :
            print "[INFO] {0}:{1} is created by failover. Failover can recreate new master for cache instance (space_id={2})".format(slave_ip_new,slave_port_new,space_id)
            break
        print "[INFO] Failover is recreating master for instance (space_id={0}) ...".format(space_id)
        time.sleep(5)

    return slave_port_new

def retry_get_new_master(space_id,master_port):
    master_ip_new = 0
    master_port_new = 0
    sql_c = init()
    while 1==1:
        master_info = sql_c.get_master_ip_port(space_id)
        master_ip_new = master_info[0]
        master_port_new = master_info[1]
        if (master_port_new != master_port) and (master_port_new != 0) :
            print "[INFO] {0}:{1} is created by failover. Failover can recreate new master for cache instance (space_id={2})".format(master_ip_new,master_port_new,space_id)
            break
        print "[INFO] Failover is recreating master for instance (space_id={0}) ...".format(space_id)
        time.sleep(5)

    return master_port_new