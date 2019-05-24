#!/usr/bin/python
# coding:utf-8

import paramiko
import os
import logging
import re
info_logger = logging.getLogger(__name__)


class SSHClient(object):
    def __init__(self, ssh_host, ssh_key=False, ssh_port=22, ssh_user="root", ssh_password=""):
        self.ssh_key = ssh_key
        self.sshHost = ssh_host
        self.sshPort = ssh_port
        self.sshUser = ssh_user
        self.password = ssh_password
        self.ssh_redis = paramiko.SSHClient()

    def init_client(self):
        self.ssh_redis.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.ssh_key is False:
            self.ssh_redis.connect(hostname=self.sshHost, port=self.sshPort, username=self.sshUser, password=self.password)
        # 测试环境用ssh_key登录，可以在办公网本地运行自动化用例，配置文件中ssh_key为true时可用
        else:
            privatekey = os.path.expanduser("./config/id_rsa")
            key = paramiko.RSAKey.from_private_key_file(privatekey)
            self.ssh_redis.connect(hostname=self.sshHost, username="root", pkey=key)

    def close_client(self):
        self.ssh_redis.close()

    def exec_command(self, command):
        self.init_client()
        stdin, stdout, stderr = self.ssh_redis.exec_command(command)
        result = stdout.readlines()
        err = stderr.readlines()
        self.close_client()
        return result, err

    def ping_redis_domain(self, domain, nlb_ip):
        print domain
        result, err = self.exec_command('ping ' + domain + ' -c 1 -W 5')
        if len(err) != 0:
            return False, err
        else:
            for r in result:
                if 'icmp_seq' in r:
                    # print r
                    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", r)
                    if ips[0] == nlb_ip:
                        return True, ''
        return False, result

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

    # redis集群docker中ping redis域名，返回是否成功
    def docker_ping_cluster_domain(self, docker_id, domain, nlb_ip):
        print domain
        # ping命令，执行一次，超时时间为5秒
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


if __name__ == '__main__':
    # ssh_client = SSHClient('116.196.119.55', ssh_user='root', ssh_password='Zhangpengyun1')
    # print ssh_client.ping_redis_domain('redis-rcf43qgkix.cn-north-1.redis.jdcloud.com', '10.0.7.246')
    ssh_client = SSHClient('10.226.134.42', ssh_user='root', ssh_password='iaas-ops!@#')
    print ssh_client.docker_ping_cluster_domain('d-d588mfugai', 'redis-am41uvc2pv.sq-test01.redis.jdcloud.com', '10.0.0.16')
