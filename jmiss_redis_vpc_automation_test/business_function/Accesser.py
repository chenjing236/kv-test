# coding:utf-8
from utils.SSHClient import *
from utils.SQLClient import *
import json


class Accesser:
    # access_type可取值docker、vm
    # docker：表示使用ap docker进行数据访问验证
    # vm：表示通过云主机进行数据访问验证
    def __init__(self, conf_obj):
        self.sql_client = SQLClient(conf_obj["mysql_host"], conf_obj["mysql_port"], conf_obj["mysql_user"],
                                    conf_obj["mysql_passwd"], conf_obj["mysql_db"])
        self.ssh_client = None
        self.ssh_key = conf_obj["ssh_key"]
        self.test_key = "key"
        self.test_value = "value"
        self.access_type = conf_obj["access_type"]
        self.vm_host = conf_obj["vm_host"]
        self.vm_passwd = conf_obj["vm_passwd"]
        self.conf_obj = conf_obj

    # 初始化ssh client
    def init_ssh_client(self, space_id):
        if self.access_type == 'vm':
            self.ssh_client = SSHClient(ssh_host=self.vm_host, ssh_password=self.vm_passwd, ssh_type=self.access_type)
            # 如果为通过vm访问，则ap_docker_id为空
            return None
        else:
            result = self.sql_client.exec_query_one("select host_ip, docker_id, overlay_ip from ap where space_id = '{0}'".format(space_id), False)
            ap_host_ip = result[0]
            ap_docker_id = result[1]
            self.ssh_client = SSHClient(ssh_host=ap_host_ip, ssh_key=self.ssh_key, ssh_type=self.access_type)
            return ap_docker_id

    # 验证通过domain访问redis
    def access_domain(self, space_id, password=None):
        result = self.sql_client.exec_query_one("select domain from space where space_id = '{0}'".format(space_id), False)
        domain = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.ssh_client.exec_redis_command(domain, "set {0} {1}".format(self.test_key, self.test_value), password, ap_docker_id)
        set_result = result[0].replace("\r", "").replace("\n", "")
        result = self.ssh_client.exec_redis_command(domain, "get {0}".format(self.test_key), password, ap_docker_id)
        get_result = result[0].replace("\r", "").replace("\n", "")
        if set_result == "OK" and get_result == self.test_value:
            return True
        else:
            return False

    # 验证通过nlb访问redis
    def access_nlb(self, space_id, password=None):
        result = self.sql_client.exec_query_one("select ip_address from nlb where space_id = '{0}'".format(space_id), False)
        nlb_ip = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.ssh_client.exec_redis_command(nlb_ip, "set {0} {1}".format(self.test_key, self.test_value), password, ap_docker_id)
        set_result = result[0].replace("\r", "").replace("\n", "")
        result = self.ssh_client.exec_redis_command(nlb_ip, "get {0}".format(self.test_key), password, ap_docker_id)
        get_result = result[0].replace("\r", "").replace("\n", "")
        if set_result == "OK" and get_result == self.test_value:
            return True
        else:
            return False

    # 验证通过所有ap访问redis
    def access_ap(self, space_id, password=None):
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.sql_client.exec_query_all("select overlay_ip from ap where space_id = '{0}'".format(space_id))
        for i in range(0, len(result)):
            ap_ip = result[i][0]
            set_result = self.ssh_client.exec_redis_command(ap_ip, "set {0} {1}".format(self.test_key, self.test_value), password, ap_docker_id)
            set_result = set_result[0].replace("\r", "").replace("\n", "")
            get_result = self.ssh_client.exec_redis_command(ap_ip, "get {0}".format(self.test_key), password, ap_docker_id)
            get_result = get_result[0].replace("\r", "").replace("\n", "")
            if set_result == "OK" and get_result == self.test_value:
                continue
            else:
                return False
        return True

    # 通过domain执行redis命令获取结果
    def domain_exec_command(self, space_id, redis_command, password=None):
        result = self.sql_client.exec_query_one("select domain from space where space_id = '{0}'".format(space_id), False)
        domain = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.ssh_client.exec_redis_command(domain, redis_command, password, ap_docker_id)
        return result

    # 通过nlb执行redis命令获取结果
    def nlb_exec_command(self, space_id, redis_command, password=None):
        result = self.sql_client.exec_query_one("select ip_address from nlb where space_id = '{0}'".format(space_id), False)
        nlb_ip = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.ssh_client.exec_redis_command(nlb_ip, redis_command, password, ap_docker_id)
        return result

    # 通过ap执行redis命令获取结果
    def ap_exec_command(self, space_id, redis_command, password=None):
        result = self.sql_client.exec_query_one("select overlay_ip from ap where space_id = '{0}'".format(space_id), False)
        ap_ip = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result = self.ssh_client.exec_redis_command(ap_ip, redis_command, password, ap_docker_id)
        return result

    # 验证直连redis访问
    # todo

    # 执行ping redis域名，并且验证与nlb ip一致
    def ping_domain(self, space_id):
        result = self.sql_client.exec_query_one("select domain from space where space_id = '{0}'".format(space_id), False)
        domain = result[0]
        result = self.sql_client.exec_query_one("select ip_address from nlb where space_id = '{0}'".format(space_id), False)
        nlb_ip = result[0]
        # 如果为通过vm访问，则ap_docker_id为空
        ap_docker_id = self.init_ssh_client(space_id)
        result, err = self.ssh_client.ping_cluster_domain(domain, nlb_ip, ap_docker_id)
        return result, err

    # 在vm中执行proxy unit test脚本
    def exec_unit_test(self, space_id):
        result = self.sql_client.exec_query_one("select domain, cluster_type from space where space_id = '{0}'".format(space_id), False)
        domain = result[0]
        cluster_type = result[1]
        self.init_ssh_client(space_id)
        result = self.ssh_client.exec_unit_test(domain, cluster_type)
        return result

    # 在vm中执行set(get)_test_keys脚本，给0-511 slot均写入数据
    # cmd_type: get or set
    def exec_slot_keys(self, space_id, cmd_type, password=None):
        # 仅支持在云主机执行，测试环境docker不允许执行
        if self.conf_obj["access_type"] == 'docker':
            return True
        result = self.sql_client.exec_query_one("select domain from space where space_id = '{0}'".format(space_id), False)
        domain = result[0]
        self.init_ssh_client(space_id)
        result, err = self.ssh_client.vm_exec_command("sh /export/redis_slot_keys/{0}_keys.sh {1} \"{2}\"".format(cmd_type, domain, password))
        if result[0] == "0\n" and len(err) == 0:
            return True
        else:
            info_logger.error("{0} slot keys failed, result is [{1}], err is [{2}]".format(cmd_type, result, err))
            return False
