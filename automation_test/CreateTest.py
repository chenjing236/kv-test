import time

import pytest
from utils.redisOps import *
from utils.tools import *


class TestBaseFunc:
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

    @pytest.mark.smoke
    def test_get_cluster(self, sql_client, web_client, created_cluster):
        # wc = WebClient(conf_obj["host"], conf_obj["pin"], conf_obj["auth_token"])
        space_id, space_info = created_cluster
        instances = sql_client.get_instances(space_id)
        assert instances is not None
        check_redis_instances(instances)
        print "check cluster success"

        # test get cluster
        status, headers, res_data = web_client.get_cluster(space_id)
        assert status == 200
        assert res_data['code'] == 1
        domain = sql_client.get_domain(space_id)
        self.check_cluster_info(res_data['attach'], space_info, instances, space_id, domain)
        print "test get cluster success"

    @pytest.mark.smoke
    def test_acl(self, sql_client, web_client, created_cluster, config):
        space_id, space_info = created_cluster
        status, capacity, password, flag, tenant_id, name, remarks = space_info
        instances = sql_client.get_instances(space_id)
        # test acl
        local_ip = get_local_ip()
        ips = [local_ip]
        # ips = ["192.168.162.16", "192.168.162.17"]
        status, headers, res_data = web_client.set_acl(space_id, ips)
        assert status == 200
        assert res_data['code'] == 1
        act_ips = sql_client.get_acl(space_id)
        assert ips == act_ips
        print "set acl success"
        time.sleep(1)
        # check ap access
        check_ap_access(config['ap_host'], config['ap_port'], password, instances[0])
        print "test ap acl success"
