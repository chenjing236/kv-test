# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryQuota:
    @pytest.mark.regression
    def test_query_quota(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查询flavor列表
        quota, used, error = query_quota_step(redis_cap)
        assert error is None
        assert quota != 0
        assert quota > used
        info_logger.info("Test query quota successfully! The max of quota is {0}, used of quota is {1}".format(quota, used))
