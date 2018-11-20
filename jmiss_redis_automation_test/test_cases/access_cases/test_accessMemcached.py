import pytest
from jmiss_memcached_vpc_automation_test.steps.MemcachedClient import *
import redis



class TestAccessMemcached:

    @pytest.mark.access
    def test_access(self, access_client, config):
        mc = access_client

        print mc.set("name", "test")

        assert "test" == mc.get("name")









