# coding:utf-8
from utils.SSHClient import *
from utils.SQLClient import *


class Accesser:
    def __init__(self, conf_obj):
        self.sql_client = SQLClient(conf_obj["mysql_host"], conf_obj["mysql_port"], conf_obj["mysql_user"],
                                    conf_obj["mysql_passwd"], conf_obj["mysql_db"])
        self.ssh_client = None
        self.test_key = "key"
        self.test_value = "value"

    # 验证通过nlb访问redis
    def access_nlb(self, space_id, password=None):
        result = self.sql_client.exec_query_one("select ip_address from nlb where space_id = '{0}'".format(space_id), False)
        nlb_ip = result[0]
        result = self.sql_client.exec_query_one("select host_ip, docker_id, overlay_ip from ap where space_id = '{0}'".format(space_id), False)
        ap_host_ip = result[0]
        ap_docker_id = result[1]
        self.ssh_client = SSHClient(ap_host_ip)
        result = self.ssh_client.exec_redis_command(ap_docker_id, nlb_ip, "set {0} {1}".format(self.test_key, self.test_value), password)
        set_result = result[0].replace("\r", "").replace("\n", "")
        result = self.ssh_client.exec_redis_command(ap_docker_id, nlb_ip, "get {0}".format(self.test_key), password)
        get_result = result[0].replace("\r", "").replace("\n", "")
        if set_result == "OK" and get_result == self.test_value:
            return True
        else:
            return False

    # 验证通过所有ap访问redis
    def access_ap(self, space_id, password=None):
        result = self.sql_client.exec_query_all("select host_ip, docker_id, overlay_ip from ap where space_id = '{0}'".format(space_id))
        for i in range(0, len(result)):
            ap_host_ip = result[i][0]
            ap_docker_id = result[i][1]
            ap_ip = result[i][2]
            self.ssh_client = SSHClient(ap_host_ip)
            set_result = self.ssh_client.exec_redis_command(ap_docker_id, ap_ip, "set {0} {1}".format(self.test_key, self.test_value), password)
            set_result = set_result[0].replace("\r", "").replace("\n", "")
            get_result = self.ssh_client.exec_redis_command(ap_docker_id, ap_ip, "get {0}".format(self.test_key), password)
            get_result = get_result[0].replace("\r", "").replace("\n", "")
            if set_result == "OK" and get_result == self.test_value:
                continue
            else:
                return False
        return True

    # 通过nlb执行redis命令获取结果
    def nlb_exec_command(self, space_id, redis_command, password=None):
        result = self.sql_client.exec_query_one("select ip_address from nlb where space_id = '{0}'".format(space_id), False)
        nlb_ip = result[0]
        result = self.sql_client.exec_query_one("select host_ip, docker_id, overlay_ip from ap where space_id = '{0}'".format(space_id), False)
        ap_host_ip = result[0]
        ap_docker_id = result[1]
        self.ssh_client = SSHClient(ap_host_ip)
        result = self.ssh_client.exec_redis_command(ap_docker_id, nlb_ip, redis_command, password)
        return result

    # 通过ap执行redis命令获取结果
    def ap_exec_command(self, space_id, redis_command, password=None):
        result = self.sql_client.exec_query_one("select host_ip, docker_id, overlay_ip from ap where space_id = '{0}'".format(space_id), False)
        ap_host_ip = result[0]
        ap_docker_id = result[1]
        ap_ip = result[2]
        self.ssh_client = SSHClient(ap_host_ip)
        result = self.ssh_client.exec_redis_command(ap_docker_id, ap_ip, redis_command, password)
        return result

    # 验证直连redis访问
