import pytest
from jmiss_redis_automation_test.utils.HttpClient import *


class TestAdminApi:

    @pytest.mark.admin
    def test_get_proxy_topo(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/getProxyTopo')
        proxy_topo_response = r.json()
        assert proxy_topo_response[u'code'] is 0
        assert proxy_topo_response[u'message'] == "All proxy topology are same"

    @pytest.mark.admin
    def test_get_all_status(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/getAllStatus')
        all_status_response = r.json()
        assert all_status_response[u'code'] is 0
        assert all_status_response[u'data']['space'] == 'Running'
        proxy_items = all_status_response[u'data']['proxy']
        print "proxy item len is %s" % str(len(proxy_items))
        for i in range(len(proxy_items)):
            assert proxy_items[i]['status'] == 'Running'
        shard_items = all_status_response[u'data']['shard']
        print "shard item len is %s" % str(len(shard_items))
        for i in range(len(shard_items)):
            assert shard_items[i]['status'] == 'Running'

    @pytest.mark.admin
    def test_check_topo(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/checkTopo')
        check_topo_response = r.json()
        assert check_topo_response[u'code'] is 0
        assert len(check_topo_response[u'data']['admin']['shards']) != 0
        assert len(check_topo_response[u'data']['admin']['proxy']) != 0

    @pytest.mark.admin
    def test_check_shard_role(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/checkShardRole')
        shard_role_response = r.json()
        assert shard_role_response[u'code'] is 0
        assert len(shard_role_response[u'data']) == 0

    @pytest.mark.admin
    def test_check_configs(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/checkConfigs')
        check_config_response = r.json()
        assert check_config_response[u'code'] is 0
        assert check_config_response[u'data']['admin'] != ""

    @pytest.mark.admin
    def test_get_slot(self, config):
        # client, resp, instance_id = init_instance
        # assert instance_id is not None

        r = HttpClient.admin_request(config, '/getSlotInfo')
        get_slot_response = r.json()
        assert get_slot_response[u'code'] is 0
        for i in range(len(get_slot_response[u'data'])):
            assert len(get_slot_response[u'data'][i]['slots_info']) != 0
            assert get_slot_response[u'data'][i]['slots_state'] != ""


if __name__ =="__main__":
    pytest.main(['test_admin.py', '-s'])
