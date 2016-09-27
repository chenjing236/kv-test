#!/usr/bin/python
# coding:utf-8
from docker import Client
from JCacheUtils import *
import json

class DockerClient(object):
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj
        self.docker_daemon_port = self.conf_obj["docker_daemon_port"]
        self.docker_version = self.conf_obj["docker_version"]

    def inspect_container(self, container_host, container_port):
        base_url = "tcp://{0}:{1}".format(container_host, self.docker_daemon_port)
        container_name = "{0}_{1}".format(container_host, container_port)
<<<<<<< HEAD
        info_logger.info("check container memsize: begin to check container:{0}".format(container_name))
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name}, all=True)
        if len(ret_containers) < 1:
            info_logger.error("check container memsize: can't find container:[{0}]".format(container_name))
            return False
        info_logger.debug("check container memsize: containers info={0}".format(json.dumps(ret_containers[0])))
        inspect = c.inspect_container(container_name)
        info_logger.debug("check container memsize: inspect_container info={0}".format(json.dumps(inspect)))
=======
        info_logger.info("check redis memsize: begin to check container:{0}".format(container_name))
        c = Client(base_url=base_url, version=self.docker_version)
        ret_containers = c.containers(filters={"name": container_name}, all=True)
        if len(ret_containers) < 1:
            info_logger.error("check redis memsize: can't find container:[{0}]".format(container_name))
            return False
        info_logger.debug("check redis memsize: containers info={0}".format(json.dumps(ret_containers[0])))
        inspect = c.inspect_container(container_name)
        info_logger.debug("check redis memsize: inspect_container info={0}".format(json.dumps(inspect)))
>>>>>>> update jmiss stability test case

        # check redis memory
        redis_memsize = inspect['Args'][3]
        cmd_memsize = inspect['Config']['Cmd'][3]
        info_logger.info("redis_memsize={0}, cmd_memsize={1}".format(redis_memsize, cmd_memsize))
        if redis_memsize != cmd_memsize:
<<<<<<< HEAD
            info_logger.error("check container memsize: check container memsize error!")
            return False
        info_logger.info("check container memsize: check container memsize success!")
=======
            info_logger.error("check redis memsize: check redis memsize error!")
            return False
        info_logger.info("check redis memsize: check redis memsize success!")
>>>>>>> update jmiss stability test case
        return True
