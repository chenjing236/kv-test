#!/usr/bin/python
# coding:utf-8
import pytest
from utils.redisOps import *
import time

# Failover&Sentinel模块的smoke test cases
class TestFailoverFunc:
    # 缓存云实例的slave被stop,failover将创建新的slave
    @pytest.mark.smoke
    def test_failover_recreate_slave(self, config, docker_client, retry,sql_client, created_cluster):
        space_id, space_info = created_cluster
        wait_time = float(config["wait_time"])
        print '[Scenario] Slave of cache instance (space_id={0}) is stopped'.format(space_id)
        # 根据space id查询instance表中缓存云实例的slave信息
        instances = sql_client.get_instances(space_id)
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]

        # master信息
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]

        epoch_origin = int(sql_client.get_epoch(space_id))

        time.sleep(wait_time)

        # 向master写入key-value
        print "[STEP] 向master({0}:{1})写入(key:value)=（{2} : {3}）".format(master_ip, master_port, "cache_test_key","cache_test_value")
        set_key_value(master_info, "cache_test_key", "cache_test_value")

        print "[STEP] Search slave info of instance (space_id={0}). Slave Info : IP:Port={1}:{2}".format(space_id, slave_ip, slave_port)

        # 链接docker服务器的守护进程，根据IP_PORT停止slave
        print "[STEP] Stop slave of cache instance （space_id={0})".format(space_id)
        docker_client.stop_container(slave_ip, slave_port)
        slave_port_new = slave_port

        print "[STEP] Failover is going to recreate new slave for instance (space_id={0}).".format(space_id)
        # 扫描数据库instance表中，对应缓存云实例的slave是否被更新了
        slave_info_new = retry.retry_get_new_container(space_id,"slave")
        slave_ip_new = slave_info_new[0]
        slave_port_new = slave_info_new[1]
        epoch = int(slave_info_new[2])

        # 验证点:faiover创建的新的slave后，拓扑结构被更新
        assert epoch > epoch_origin
        time.sleep(wait_time)

        # 从新的slave中读取slave被stop前写入master的数据
        instances = sql_client.get_instances(space_id)
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]
        value = get_value(slave_info, "cache_test_key")
        print "[STEP] 从slave({0}:{1})获取cache_test_key的value={2}".format(slave_ip, slave_port, value)
        assert "cache_test_value" == value

        # 删除key-value
        print "[STEP] 从slave({0}:{1})删除cache_test_key".format(slave_ip, slave_port)
        delete_key_value(master_info, "cache_test_key")
        value = get_value(slave_info, "cache_test_key")
        assert value is None

        #获取instance主从信息
        master_redis_info = get_redis_info(master_ip, master_port)
        slave_redis_host = master_redis_info["slave0"]["ip"]
        slave_redis_port = master_redis_info["slave0"]["port"]
        print "[INFO] Redis information of slave for instance({0}) is {1}:{2}. Information of slave is {3}:{4}".format(space_id,slave_redis_host,slave_redis_port,slave_ip,slave_port)
        assert slave_redis_host == slave_ip and  slave_redis_port == slave_port

    # 缓存云实例的master被stop,failover将创建新的master
    @pytest.mark.smoke
    def test_failover_recreate_master(self, config, docker_client, retry, sql_client, created_cluster):
        space_id, space_info = created_cluster
        wait_time = float(config["wait_time"])
        print "[Scenario] Master of cache instance (space_id={0}) is stopped".format(space_id)
        # 根据space id查询instance表中缓存云实例的master信息
        instances = sql_client.get_instances(space_id)
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]

        # slave信息
        slave_info = instances[1]
        slave_ip = slave_info[0]
        slave_port = slave_info[1]

        epoch_origin = int(sql_client.get_epoch(space_id))

        time.sleep(wait_time)

        print "[STEP] 向master({0}:{1})写入key-value=（{2}-{3}）".format(master_ip, master_port, "cache_test_key", "cache_test_value")
        set_key_value(master_info, "cache_test_key", "cache_test_value")

        print "[STEP] Search master info of instance (space_id={0}). Master Info : IP:Port={1}:{2}".format(
            space_id, master_ip, master_port)

        # 链接docker服务器的守护进程，根据IP_PORT停止master
        print "[STEP] Stop master of cache instance （space_id={0})".format(space_id)
        docker_client.stop_container(master_ip, master_port)
        master_port_new = master_port

        print "[STEP] Failover is going to recreate new master for instance (space_id={0}).".format(space_id)
        # 扫描数据库instance表中，对应缓存云实例的master是否被更新了
        master_info_new = retry.retry_get_new_container(space_id,"master")
        master_ip_new = master_info_new[0]
        master_port_new = master_info_new[1]
        epoch = int(master_info_new[2])

        # 验证点:faiover创建的新的master后，拓扑结构被更新
        assert epoch > epoch_origin
        time.sleep(wait_time)

        # 获取stop master前写入master的key-value
        value = get_value(slave_info, "cache_test_key")
        print "[STEP] 从slave({0}:{1})获取cache_test_key的value={2}".format(slave_ip, slave_port, value)
        assert "cache_test_value" == value

        # 向新的master写入数据
        instances = sql_client.get_instances(space_id)
        master_info = instances[0]
        master_ip = master_info[0]
        master_port = master_info[1]
        print "[STEP] 向master({0}:{1})写入(key:value)=（{2} : {3}）".format(master_ip, master_port, "cache_test_key_1", "cache_test_value_1")
        set_key_value(master_info, "cache_test_key_1", "cache_test_value_1")

        print "[STEP] 从slave({0}:{1})删除cache_test_key".format(slave_ip, slave_port)
        delete_key_value(master_info, "cache_test_key")
        value = get_value(slave_info, "cache_test_key")
        assert value is None

        print "[STEP] 从slave({0}:{1})删除cache_test_key_1".format(slave_ip, slave_port)
        delete_key_value(master_info, "cache_test_key_1")
        value = get_value(slave_info, "cache_test_key_1")
        assert value is None

        #获取instance主从信息
        slave_redis_info = get_redis_info(slave_ip, slave_port)
        master_redis_host = slave_redis_info["master_host"]
        master_redis_port = slave_redis_info["master_port"]
        print "[INFO] Master information of master for instance({0}) is {1}:{2}. Information of slave is {3}:{4}".format(space_id,master_redis_host,master_redis_port,master_ip,master_port)
        assert master_redis_host == master_ip and master_redis_port == master_port

        # # 验证failover不创建新的master和slave的时间过长
        # # 缓存云实例的master和slave同时被stop,failover不创建新的master和slave
        # @pytest.mark.smoke
        # def test_stop_master_and_slave(self, config, docker_client, retry, sql_client, created_cluster):
        #     space_id, space_info = created_cluster
        #     wait_time = float(config["wait_time"])
        #     print "[Scenario] Master of cache instance (space_id={0}) is stopped".format(space_id)
        #     # 根据space id查询instance表中缓存云实例的master信息
        #     instances = sql_client.get_instances(space_id)
        #     master_info = instances[0]
        #     master_ip = master_info[0]
        #     master_port = master_info[1]
        #
        #     # slave信息
        #     slave_info = instances[1]
        #     slave_ip = slave_info[0]
        #     slave_port = slave_info[1]
        #
        #     epoch_origin = int(sql_client.get_epoch(space_id))
        #     time.sleep(wait_time)
        #
        #     print "[STEP] 向master({0}:{1})写入key-value=（{2}-{3}）".format(master_ip, master_port, "cache_test_key",
        #                                                                 "cache_test_value")
        #     set_key_value(master_info, "cache_test_key", "cache_test_value")
        #
        #     print "[STEP] Search master info of instance (space_id={0}). Master Info : IP:Port={1}:{2}".format(
        #         space_id, master_ip, master_port)
        #
        #     # 链接docker服务器的守护进程，根据IP_PORT同时停止master和slave
        #     print "[STEP] Stop master of cache instance （space_id={0})".format(space_id)
        #     docker_client.stop_container(master_ip, master_port)
        #     docker_client.stop_container(slave_ip, slave_port)
        #     master_port_new = master_port
        #
        #     print "[STEP] Failover is going to recreate new master for instance (space_id={0}).".format(space_id)
        #     # 扫描数据库instance表中，对应缓存云实例的master是否被更新了
        #
        #     master_info_new = retry.retry_get_new_container(space_id, "master")
        #     master_ip_new = master_info_new[0]
        #     master_port_new = master_info_new[1]
        #     epoch = int(master_info_new[2])
        #
        #     # 验证点:faiover创建的新的master后，拓扑结构被更新
        #     assert epoch == epoch_origin
        #     time.sleep(wait_time)
        #
        #     # 获取stop master前写入master的key-value
        #     value = get_value(slave_info, "cache_test_key")
        #     print "[STEP] 从slave({0}:{1})获取cache_test_key的value={2}".format(slave_ip, slave_port, value)
        #     assert "cache_test_value" == value
        #
        #     # 向新的master写入数据
        #     # instances = sql_client.get_instances(space_id)
        #     # master_info = instances[0]
        #     # master_ip = master_info[0]
        #     # master_port = master_info[1]
        #     # print "[STEP] 向master({0}:{1})写入(key:value)=（{2} : {3}）".format(master_ip, master_port, "cache_test_key_1",
        #     #                                                                 "cache_test_value_1")
        #     # set_key_value(master_info, "cache_test_key_1", "cache_test_value_1")
        #     #
        #     # print "[STEP] 从slave({0}:{1})删除cache_test_key".format(slave_ip, slave_port)
        #     # delete_key_value(master_info, "cache_test_key")
        #     # value = get_value(slave_info, "cache_test_key")
        #     # assert value is None
        #     #
        #     # print "[STEP] 从slave({0}:{1})删除cache_test_key_1".format(slave_ip, slave_port)
        #     # delete_key_value(master_info, "cache_test_key_1")
        #     # value = get_value(slave_info, "cache_test_key_1")
        #     # assert value is None
        #
        #     # 获取instance主从信息
        #     slave_redis_info = get_redis_info(slave_ip, slave_port)
        #     master_redis_host = slave_redis_info["master_host"]
        #     master_redis_port = slave_redis_info["master_port"]
        #     print "[INFO] Master information of master for instance({0}) is {1}:{2}. Information of slave is {3}:{4}".format(
        #         space_id, master_redis_host, master_redis_port, master_ip, master_port)
        #     assert master_redis_host == master_ip and master_redis_port == master_port
