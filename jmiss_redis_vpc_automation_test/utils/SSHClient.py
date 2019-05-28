#!/usr/bin/python
# coding:utf-8

import paramiko
import os
import re
import logging

info_logger = logging.getLogger(__name__)


class SSHClient(object):
    def __init__(self, ssh_host, ssh_key=False, ssh_port=22, ssh_user="root", ssh_password="", ssh_type='docker'):
        self.ssh_key = ssh_key
        self.sshHost = ssh_host
        self.sshPort = ssh_port
        self.sshUser = ssh_user
        self.password = ssh_password
        # ssh_type用于区分在vm和docker中执行命令
        # docker：用于测试或预发环境
        # vm：用于线上或预发环境
        self.ssh_type = ssh_type
        self.ssh_redis = paramiko.SSHClient()
        logging.getLogger("paramiko").setLevel(logging.WARNING)

    def init_client(self):
        self.ssh_redis.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.ssh_key is False:
            self.ssh_redis.connect(hostname=self.sshHost, port=self.sshPort, username=self.sshUser,
                                   password=self.password)
        # 测试环境用ssh_key登录，可以在办公网本地运行自动化用例，配置文件中ssh_key为true时可用
        else:
            privatekey = os.path.expanduser("./config/id_rsa")
            key = paramiko.RSAKey.from_private_key_file(privatekey)
            self.ssh_redis.connect(hostname=self.sshHost, username="root", pkey=key)
        # 不输出paramiko info级别日志
        # logging.getLogger("paramiko").setLevel(logging.WARNING)

    def close_client(self):
        self.ssh_redis.close()

    # 用于在云主机中执行shell命令
    def vm_exec_command(self, command):
        self.init_client()
        stdin, stdout, stderr = self.ssh_redis.exec_command(command)
        result = stdout.readlines()
        err = stderr.readlines()
        self.close_client()
        return result, err

    # 用于在redis集群docker中执行shell命令
    def docker_exec_command(self, docker_id, command):
        self.init_client()
        # /opt/jmiss-redis-aproxy/redis-cli -h ip -a 'passwd' get key
        command = "docker ps -a | grep {0} | awk '{{print $1}}' | xargs -i docker exec -i {{}} bash -c \"{1}\"".format(
            docker_id, command)
        stdin, stdout, stderr = self.ssh_redis.exec_command(command)
        result = stdout.readlines()
        err = stderr.readlines()
        self.close_client()
        return result, err

    # vm/docker中执行redis命令
    def exec_redis_command(self, ip, redis_command, password='', docker_id=None):
        if self.ssh_type == 'vm':
            command = "redis-cli -h {0} -a \'{1}\' {2}".format(ip, password, redis_command)
            result, err = self.vm_exec_command(command)
        else:
            command = "/opt/jmiss-redis-aproxy/redis-cli -h {0} -a \'{1}\' {2}".format(ip, password, redis_command)
            result, err = self.docker_exec_command(docker_id, command)
        if len(err) != 0:
            assert False, info_logger.error("[ERROR] Failed to exec redis command, the error is {0}".format(err))
        return result

    # vm/docker中ping redis域名，返回是否成功
    def ping_cluster_domain(self, domain, nlb_ip, docker_id=None):
        # ping命令，执行一次，超时时间为5秒
        if self.ssh_type == 'vm':
            result, err = self.vm_exec_command('ping ' + domain + ' -c 1 -W 5')
        else:
            result, err = self.docker_exec_command(docker_id, 'ping ' + domain + ' -c 1 -W 5')
        if len(err) != 0:
            return False, err
        else:
            for r in result:
                if 'icmp_seq' in r:
                    # print r
                    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", r)
                    # 验证ping域名的结果与nlb ip一致
                    if ips[0] == nlb_ip:
                        return True, None
        return False, result

    # vm中执行redis unit test，docker中暂不支持执行
    def exec_unit_test(self, ip, cluster_type):
        if self.ssh_type == 'vm':
            command = "sh /export/redis_unit_test/run {0} {1}".format(ip, cluster_type)
            result, err = self.vm_exec_command(command)
        else:
            # 暂不支持在docker中执行unit test，当前跳过
            return True
        # unit test执行成功，返回值为0
        if len(err) != 0:
            print result, err
            return False
        if result[0] == "0\n":
            return True
        # unit test执行失败，返回值不为0
        else:
            return False

    # 在redis docker中执行访问命令
    # 使用exec_redis_command方法
    #
    # def redis_get_key(self, docker_id, ip, key, password=None):
    #     redis_command = "get " + key
    #     result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
    #     return result, err
    #
    # def redis_set_key(self, docker_id, ip, key, value, password=None):
    #     redis_command = "set " + key + " " + value
    #     result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
    #     return result, err
    #
    # def redis_delete_key(self, docker_id, ip, key, password=None):
    #     redis_command = "del " + key
    #     result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
    #     return result, err
