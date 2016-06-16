import pytest
from utils.SQLClient import SQLClient
from utils.WebClient import *
from utils.redisOps import *
from utils.JCacheUtils import *
from utils.tools import *
import json
import time

conf_path = "./conf.json"
conf_obj = json.load(open(conf_path, 'r'))


class TestBaseFunc:
    def setup_class(self):
        self.conf_obj = json.load(open(conf_path, 'r'))
        self.teardown_space_list = []
        self.wc = WebClient(conf_obj["host"], conf_obj["pin"], conf_obj["auth_token"])
        self.sql_c = SQLClient(conf_obj['mysql_host'], conf_obj["mysql_port"], conf_obj["mysql_user"],
                               conf_obj["mysql_passwd"],
                               conf_obj["mysql_db"])
        self.ca = CreateArgs(2097152, 1, "create_test", "create_cluster", 1, 1)
        self.space_id, self.space_info = CreateCluster(self.wc, self.ca, self.teardown_space_list, self.sql_c)

    def teardown_class(self):
        for space in self.teardown_space_list:
            DeleteCluster(self.wc, space, self.sql_c)

    def compare_instance(self, jinstance, jinstance_expect, space_id):
        ip, port, copy_id, flag = jinstance_expect
        assert jinstance['ip'] == ip
        assert jinstance['port'] == port
        assert jinstance['copyId'] == copy_id
        assert jinstance['flag'] == flag
        assert jinstance['spaceId'] == space_id

    def check_cluster_info(self, cluster, space, instances, space_id, domian):
        status, capacity, password, flag, tenant_id, name, remarks = space
        assert cluster['status'] == status
        assert cluster['flag'] == flag
        assert cluster['capacity'] == capacity
        assert cluster['password'] == password + str(space_id)
        assert cluster['tenantId'] == tenant_id
        assert cluster['name'] == name
        assert cluster['remarks'] == remarks
        assert cluster['id'] == space_id
        assert cluster['domain'] == domian
        jinstance = cluster['instances']
        assert len(jinstance) == 2
        if jinstance[0]['copyId'] != 'm':
            tmp = jinstance[0]
            jinstance[0] = jinstance[1]
            jinstance[1] = tmp
        self.compare_instance(jinstance[0], instances[0], space_id)
        self.compare_instance(jinstance[1], instances[1], space_id)

    def test_get_cluster(self):
        # wc = WebClient(conf_obj["host"], conf_obj["pin"], conf_obj["auth_token"])

        instances = self.sql_c.get_instances(self.space_id)
        assert instances is not None
        check_redis_instances(instances)
        print "check cluster success"

        # test get cluster
        status, headers, res_data = self.wc.get_cluster(self.space_id)
        assert status == 200
        assert res_data['code'] == 1
        domain = self.sql_c.get_domain(self.space_id)
        self.check_cluster_info(res_data['attach'], self.space_info, instances, self.space_id, domain)
        print "test get cluster success"

    def test_acl(self):
        status, capacity, password, flag, tenant_id, name, remarks = self.space_info
        instances = self.sql_c.get_instances(self.space_id)
        # test acl
        # local_ip = get_local_ip()
        # ips = [local_ip]
        ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = self.wc.set_acl(self.space_id, ips)
        assert status == 200
        assert res_data['code'] == 1
        act_ips = self.sql_c.get_acl(self.space_id)
        assert ips == act_ips
        print "set acl success"
        time.sleep(1)
        # check ap access
        check_ap_access(conf_obj['ap_host'], conf_obj['ap_port'], password + str(self.space_id), instances[0])
        print "test ap acl success"
