import pytest
from jmiss_redis_automation_test.utils.SqlConst import *



class TestAccessMemcached:

    @pytest.mark.access
    # @pytest.mark.openapi
    def test_access(sself, init_instance, config):
        # print sql_const.QUERY_INSTANCE
        client, resp, instance_id = init_instance
        assert instance_id is not None








