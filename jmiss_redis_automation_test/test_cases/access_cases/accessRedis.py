import pytest
from jmiss_redis_automation_test.utils.SqlConst import *



class TestAccessMemcached:

    @pytest.mark.access
    def test_access(self):
        print sql_const.QUERY_INSTANCE
        print sql_const.DSFA







