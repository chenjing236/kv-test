#!/usr/bin/python
# coding:utf-8

import paramiko
from conftest import *


class SSHClient(object):
    def __init__(self, ssh_host, ssh_port=22, ssh_user="root", ssh_password=""):
        self.sshHost = ssh_host
        self.sshPort = ssh_port
        self.sshUser = ssh_user
        self.password = ssh_password
        self.ssh_redis = paramiko.SSHClient()

    def init_client(self):
        self.ssh_redis.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_redis.connect(hostname=self.sshHost, port=self.sshPort, username=self.sshUser, password=self.password)

    def close_client(self):
        self.ssh_redis.close()

    def exec_redis_command(self, docker_id, ip, redis_command, password=None):
        self.init_client()
        # /opt/jmiss-redis-aproxy/redis-cli -h ip get key
        # no password or use redis
        if password is None:
            command = "docker ps -a | grep {0} | awk '{{print $1}}' | xargs -i docker exec -i {{}} " \
                    "bash -c \"/opt/jmiss-redis-aproxy/redis-cli -h {1} {2}\"".format(
                     docker_id, ip, redis_command)
        # use password
        else:
            command = "docker ps -a | grep {0} | awk '{{print $1}}' | xargs -i docker exec -i {{}} " \
                      "bash -c \"/opt/jmiss-redis-aproxy/redis-cli -h {1} -a {2} {3}\"".format(
                       docker_id, ip, password, redis_command)
        stdin, stdout, stderr = self.ssh_redis.exec_command(command)
        result = stdout.readlines()
        err = stderr.readlines()
        self.close_client()
        if len(err) != 0:
            info_logger.info("[ERROR] Failed to exec redis command, the error is {0}".format(err))
            assert False
        return result

    def redis_get_key(self, docker_id, ip, key, password=None):
        self.init_client()
        redis_command = "get " + key
        result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
        self.close_client()
        return result, err

    def redis_set_key(self, docker_id, ip, key, value, password=None):
        self.init_client()
        redis_command = "set " + key + " " + value
        result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
        self.close_client()
        return result, err

    def redis_delete_key(self, docker_id, ip, key, password=None):
        self.init_client()
        redis_command = "del " + key
        result, err = self.exec_redis_command(docker_id, ip, redis_command, password)
        self.close_client()
        return result, err
