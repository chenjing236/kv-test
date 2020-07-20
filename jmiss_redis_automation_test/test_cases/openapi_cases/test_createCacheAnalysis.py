from jmiss_redis_automation_test.steps.CacheAnalysisOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import create_cache_analysis, baseCheckPoint
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance
from jmiss_redis_automation_test.steps.Valification import assertRespNotNone
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_redis_configmap
import pytest


class TestCreateCacheAnalysis:
    def test_create_cacheAnalysis(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instance_id = create_validate_instance(config, instances[0], expected_object)

        resp = create_cache_analysis(config, instance_id, client)
        assertRespNotNone(resp)

        expected_object.space_status="KeyAnalysising"
        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["shardNumber"])

    @pytest.mark.cacheAnalysis
    def test_modify_cache_Analysis_time(self, config, instance_data, expected_data):
        instances = instance_data["create_standard_specified"]
        expected_object = baseCheckPoint(expected_data[instances[0]["cacheInstanceClass"]],
                                         instances[0]["instance_password"])
        client, _, instance_id = create_validate_instance(config, instances[0], expected_object)

        time= "01:00-02:00 +0800"

        resp = modify_cache_analysis_time(config, instance_id,time,client)
        assertRespNotNone(resp)

        assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instances[0]["shardNumber"])
        resp=query_cache_analysis_time(config,instance_id)

        assert resp.result["time"]==time
