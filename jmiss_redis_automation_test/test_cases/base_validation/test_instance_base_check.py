from jmiss_redis_automation_test.steps.InstanceOperation import *


class TestInstanceBasecheck:
    @pytest.mark.basecheck
    def test_standard_base_check(self, config, instance_data, expected_data):
        expected_object = baseCheckPoint(expected_data["redis.s.micro.basic"], "")

        assert check_admin_proxy_redis_configmap("redis-h242hp75jemy", config, expected_object, 1)

