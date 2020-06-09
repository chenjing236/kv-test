from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.WebCommand import *


@pytest.mark.intergration
def test_standard_expansion(self, config, instance_data, expected_data):
    modify_instance = instance_data["modify_standard_instance"]
    client, _, instance_id = create_validate_instance(config, modify_instance, expected_data)
    resp = reset_validate_class(config, instance_id, modify_instance["target_cacheInstanceClass"], client,
                                modify_instance["target_shardNumber"])

    if instance_id is not None:
        delete_instance(config, instance_id, client)


@pytest.mark.intergration
def test_cluster_expansion(self, config, instance_data, expected_data):
    modify_instance = instance_data["modify_cluster_instance"]
    client, _, instance_id = create_validate_instance(config, modify_instance, expected_data)
    resp = reset_validate_class(config, instance_id, modify_instance["target_cacheInstanceClass"], client,
                                modify_instance["target_shardNumber"])

    if instance_id is not None:
        delete_instance(config, instance_id, client)


@pytest.mark.intergration
def test_standard_to_cluster(self, config, instance_data, expected_data):
    modify_instance = instance_data["modify_standard_to_cluster_instance"]
    client, _, instance_id = create_validate_instance(config, modify_instance, expected_data)
    resp = reset_validate_class(config, instance_id, modify_instance["target_cacheInstanceClass"], client,
                                modify_instance["target_shardNumber"])

    if instance_id is not None:
        delete_instance(config, instance_id, client)


@pytest.mark.intergration
def test_cluster_to_standard(self, config, instance_data, expected_data):
    modify_instance = instance_data["modify_cluster_to_standard_instance"]
    client, _, instance_id = create_validate_instance(config, modify_instance, expected_data)
    resp = reset_validate_class(config, instance_id, modify_instance["target_cacheInstanceClass"], client,
                                modify_instance["target_shardNumber"])

    if instance_id is not None:
        delete_instance(config, instance_id, client)


@pytest.mark.stability
def test_resize_webcli(self, config, instance_data, expected_data):
    instance = instance_data["modify_standard_instance"]

    expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                     instance["instance_password"])
    client, _, instance_id = create_validate_instance(config, instance, expected_object)

    resp = reset_validate_class(config, instance_id, instance["target_cacheInstanceClass"], client,
                                instance["target_shardNumber"])

    expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],
                                     instance["instance_password"])
    expected_object.side = 1
    expected_object.current_rs_type = "b"
    expected_object.next_rs_type = "a"

    resp = send_web_command(config, instance_id, config["region"], "auth " + instance["instance_password"])
    token = resp.result["token"]
    object = WebCommand(config, instance_id, config["region"], token)
    object.checkAllCommand()

    assert check_admin_proxy_redis_configmap(instance_id, config, expected_object, instance["target_shardNumber"])
