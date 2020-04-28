from jmiss_redis_automation_test.steps.FusionOpertation import *


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