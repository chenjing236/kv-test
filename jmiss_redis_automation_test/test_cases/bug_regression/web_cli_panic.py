import pytest

from jmiss_redis_automation_test.steps.InstanceOperation import *


class TestCreateInstanceNobill:

    @pytest.mark.createnobill
    def test_cli_createInstanceNobill(self, config, instance_data, expected_data):
        instance = instance_data["create_standard_specified"][0]
        client, resp, instance_id = create_validate_instance(config, instance, expected_data)

        instance = None
        if resp.error is None and instance_id is not None:
            instance = query_instance_recurrent(200, 5, instance_id, config, client)
            config["request_id"] = resp.request_id
        else:
            config["request_id"] = ""

        assert instance_id is not None
        time.sleep(1)

        if instance_id is not None:
            delete_instance(config, instance_id, client)
