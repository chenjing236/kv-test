import time

import pytest
from utils.redisOps import *
from utils.tools import *
from utils.JCacheUtils import *


class TestBaseFunc:

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
        CheckClusterInfo(res_data['attach'], space_info, instances, space_id, domain)
        print "test get cluster success"

    @pytest.mark.smoke
    def test_acl(self, sql_client, web_client, created_cluster, config):
        print "begin to test acl"
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
