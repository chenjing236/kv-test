# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestQueryFlavor:
    @pytest.mark.regression
    def test_query_flavor(self, config, instance_data):
        redis_cap = RedisCap(config, instance_data)
        # 查询flavor列表
        flavor_list, error = query_flavor_step(redis_cap)
        assert error is None
        assert len(flavor_list) != 0
        info_logger.info("Test query flavor successfully!")
