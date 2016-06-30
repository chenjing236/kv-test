#!/usr/bin/python
#coding:utf-8
import pytest
from utils.tools import *
from utils.DockerContainerOps import DockerClient
from utils.Retry import Retry
from utils.WebClient import *
from utils.SQLClient import SQLClient
from utils.JCacheUtils import *
from utils.redisOps import *
import json
from docker import Client
import string
import time

#获取conf.json的绝对路径
conf_path = cur_file_dir() + "\conf.json"
conf_obj = json.load(open(conf_path, 'r'))
#Docker守护进程的port
container_daemon = conf_obj['docker_daemon']

#获取data.json的绝对路径,数据驱动
data_path = cur_file_dir() + "\instance_data.json"
data_obj = json.load(open(data_path, 'r'))

retry_times = int(conf_obj['retry_times'])

wait_time = float(conf_obj['wait_time'])

#Failover&Sentinel模块的smoke test cases
class TestFailoverFunc:

    #创建缓存云实例
    def setup_class(self):
        print "[STEP] Create instance for cache"
        self.docker_c = DockerClient(conf_path)
        self.retry = Retry(conf_path)
        self.teardown_space_list = []
        self.wc = WebClient(conf_obj["host"], conf_obj["pin"], conf_obj["auth_token"])
        self.sql_c = SQLClient(conf_obj['mysql_host'], conf_obj["mysql_port"], conf_obj["mysql_user"],
                               conf_obj["mysql_passwd"],
                               conf_obj["mysql_db"])
        self.ca = CreateArgs(data_obj['capacity'],data_obj['zoneId'], data_obj['remarks'], data_obj['spaceName'], data_obj['spaceType'],data_obj['quantity'])
        self.space_id, self.space_info = CreateCluster(self.wc, self.ca, self.teardown_space_list, self.sql_c)
        print "[INFO] Instance (space_id={0}) is created successfully.".format(self.space_id)

    #删除缓存云实例
    def teardown_class(self):
        print "[STEP] Delete instance of cache"
        for space in self.teardown_space_list:
             DeleteCluster(self.wc, space, self.sql_c)

    #缓存云实例的slave被stop,failover将创建新的slave
    @pytest.mark.smoke
    def test_failover_recreate_slave(self):
        print '[Scenario] Slave of cache instance (space_id={0}) is stopped'.format(self.space_id)
        #根据space id查询instance表中缓存云实例的slave信息
        instances = self.sql_c.get_instances(self.space_id)
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]

        #master信息
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]

        #向master写入key-value
        print "[STEP] 向master({0}:{1})写入key-value=（{2}-{3}）".format(master_ip,master_port,"cache_test_key","cache_test_value")
        set_key_value(master_info,"cache_test_key","cache_test_value")

        print "[STEP] Search slave info of instance (space_id={0}). Slave Info : IP:Port={1}:{2}".format(self.space_id,slave_ip, slave_port)

        #链接docker服务器的守护进程，根据IP_PORT停止slave
        print "[STEP] Stop slave of cache instance （space_id={0})".format(self.space_id)
        self.docker_c.stop_slave(self.space_id,slave_ip,slave_port,container_daemon)
        slave_port_new = slave_port

        print "[STEP] Failover is going to recreate new slave for instance (space_id={0}).".format(self.space_id)
        #扫描数据库instance表中，对应缓存云实例的slave是否被更新了
        slave_port_new = self.retry.retry_get_new_slave(self.space_id,slave_ip,slave_port,retry_times)

        #验证点:faiover创建的新的slave的Port与最初的slave的Port不同
        assert slave_port_new != slave_port

        #从新的slave中读取slave被stop前写入master的数据
        instances = self.sql_c.get_instances(self.space_id)
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]
        value = get_value_from_slave(slave_info,"cache_test_key")
        print "[STEP] 从slave({0}:{1})获取cache_test_key的value={2}".format(slave_ip,slave_port,value)
        assert "cache_test_value" == value

        #删除key-value
        print "[STEP] 从slave({0}:{1})删除cache_test_key".format(slave_ip,slave_port)
        delete_key_value(master_info,"cache_test_key")
        value = get_value_from_slave(slave_info,"cache_test_key")
        assert value is None

    #缓存云实例的master被stop,failover将创建新的master
    @pytest.mark.smoke
    def test_failover_recreate_master(self):
        print "[Scenario] Master of cache instance (space_id={0}) is stopped".format(self.space_id)
        #根据space id查询instance表中缓存云实例的master信息
        instances = self.sql_c.get_instances(self.space_id)
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]

        #slave信息
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]

        print "[STEP] 向master({0}:{1})写入key-value=（{2}-{3}）".format(master_ip,master_port,"cache_test_key","cache_test_value")
        set_key_value(master_info,"cache_test_key","cache_test_value")

        print "[STEP] Search master info of instance (space_id={0}). Master Info : IP:Port={1}:{2}".format(self.space_id,master_ip, master_port)

        #链接docker服务器的守护进程，根据IP_PORT停止master
        print "[STEP] Stop master of cache instance （space_id={0})".format(self.space_id)
        self.docker_c.stop_master(self.space_id,master_ip,master_port,container_daemon)
        master_port_new = master_port

        print "[STEP] Failover is going to recreate new master for instance (space_id={0}).".format(self.space_id)
        #扫描数据库instance表中，对应缓存云实例的master是否被更新了
        master_port_new = self.retry.retry_get_new_master(self.space_id,master_ip,master_port,retry_times)

        #验证点:faiover创建的新的master的Port与最初的master的Port不同
        assert master_port_new != master_port
        time.sleep(wait_time)

        #获取stop master前写入master的key-value
        value = get_value_from_slave(slave_info,"cache_test_key")
        print "[STEP] 从slave({0}:{1})获取cache_test_key的value={2}".format(slave_ip,slave_port,value)
        assert "cache_test_value" == value

        #向新的master写入数据
        instances = self.sql_c.get_instances(self.space_id)
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]
        print "[STEP] 向master({0}:{1})写入key-value=（{2}-{3}）".format(master_ip,master_port,"cache_test_key_1","cache_test_value_1")
        set_key_value(master_info,"cache_test_key_1","cache_test_value_1")

        print "[STEP] 从slave({0}:{1})删除cache_test_key".format(slave_ip,slave_port)
        delete_key_value(master_info,"cache_test_key")
        value = get_value_from_slave(slave_info,"cache_test_key")
        assert value is None

        print "[STEP] 从slave({0}:{1})删除cache_test_key_1".format(slave_ip,slave_port)
        delete_key_value(master_info,"cache_test_key_1")
        value = get_value_from_slave(slave_info,"cache_test_key_1")
        assert value is None
