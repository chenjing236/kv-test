# coding:utf-8
from BasicTestCase import *
import logging
info_logger = logging.getLogger(__name__)


class TestCreateApi:
    @pytest.mark.regression
    def test_create_with_empty_vpc_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["vpcId"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty vpc_id successfully!")

    @pytest.mark.regression
    def test_create_with_error_vpc_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["vpcId"] = "vpc-error"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test create master-slave instance with error vpc_id successfully!")

    @pytest.mark.regression
    def test_create_with_empty_subnet_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["subnetId"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty subnet_id successfully!")

    @pytest.mark.regression
    def test_create_with_error_subnet_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["subnetId"] = "subnet-error"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test create master-slave instance with error subnet_id successfully!")

    @pytest.mark.regression
    def test_create_with_empty_instance_class(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceClass"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty instance_class successfully!")

    @pytest.mark.regression
    def test_create_with_error_instance_class(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceClass"] = "redis.error"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test create master-slave instance with error instance_class successfully!")

    @pytest.mark.regression
    def test_create_with_empty_name(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceName"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        # 查看redis详情，验证缓存云实例状态，status=running, 验证基本信息正确
        cluster_detail, error = query_detail_step(redis_cap, space_id)
        assert cluster_detail["cacheInstanceStatus"] == "running"
        assert cluster_detail["cacheInstanceName"] == space_id
        info_logger.info("Test create master-slave instance with empty name successfully!")

        # 删除实例
        delete_step(redis_cap, space_id)
        time.sleep(5)

    # todo: name为空，创建成功，name为默认space_id
    # todo: name包含中文，创建成功，name设置正确
    # todo: name包含数字，创建成功，name设置正确
    # todo: name包含大小写字母，创建成功，name设置正确
    # todo: name包含下划线“_”，创建成功，name设置正确
    # todo: name包含中划线"-"，创建成功，name设置正确
    # todo: name为2字符，创建成功，name设置正确
    # todo: name为32字符，创建成功，name设置正确

    @pytest.mark.regression
    def test_create_with_name_shorter_than_2(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceName"] = "1"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with name shorter than 2 successfully!")

    @pytest.mark.regression
    def test_create_with_name_longer_than_32(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceName"] = "1" * 33
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with name longer than 32 successfully!")

    @pytest.mark.regression
    def test_create_with_name_include_special_signal(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceName"] = "signal@"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with name include special signal successfully!")

    # todo: description为空，创建成功
    # todo: description长度小于256，创建成功

    @pytest.mark.regression
    def test_create_with_remarks_longer_than_256(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["cacheInstanceDescription"] = "1" * 257
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with remarks longer than 256 successfully!")

    # todo: password长度为8，创建成功
    # todo: password长度为16，创建成功

    @pytest.mark.regression
    def test_create_with_pwd_shorter_than_8(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["password"] = "1qaz2WS"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with password shorter than 8 successfully!")

    @pytest.mark.regression
    def test_create_with_pwd_longer_than_16(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["password"] = "1qaz2WSX1qaz2WSX1"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with password longer than 16 successfully!")

    @pytest.mark.regression
    def test_create_with_pwd_not_contain_capital_letters(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["password"] = "1qaz2wsx"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with password not contain capital letters successfully!")

    @pytest.mark.regression
    def test_create_with_pwd_not_contain_lowercase_letters(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["password"] = "1QAZ2WSX"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with password not contain lowercase letters successfully!")

    @pytest.mark.regression
    def test_create_with_pwd_not_contain_numbers(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["password"] = "qazWSXed"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with password not contain numbers successfully!")

    @pytest.mark.regression
    def test_create_with_empty_az_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["azId"] = {}
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty az_id successfully!")

    @pytest.mark.regression
    def test_create_with_empty_master_az_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["azId"]["master"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty master az_id successfully!")

    @pytest.mark.regression
    def test_create_with_empty_slave_az_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["azId"]["slave"] = ""
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with empty slave az_id successfully!")

    @pytest.mark.regression
    def test_create_with_error_az_id(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["azId"]["master"] = "error"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        info_logger.info("Test create master-slave instance with error az_id successfully!")

    @pytest.mark.regression
    def test_create_with_error_redis_version(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        create_params["redisVersion"] = "1.0"
        space_id, error = create_step(redis_cap, create_params, None)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with error redis version successfully!")

    @pytest.mark.regression
    def test_create_with_error_charge_mode(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        charge_params["chargeMode"] = "error_mode"
        space_id, error = create_step(redis_cap, create_params, charge_params)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with error charge mode successfully!")

    @pytest.mark.regression
    def test_create_with_error_charge_unit(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        charge_params["chargeUnit"] = "error_unit"
        space_id, error = create_step(redis_cap, create_params, charge_params)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with error charge unit successfully!")

    @pytest.mark.regression
    def test_create_with_error_charge_duration(self, config, instance_data, get_create_params):
        # 创建缓存云实例
        redis_cap = RedisCap(config, instance_data)
        create_params, charge_params = get_create_params
        charge_params["chargeDuration"] = 0
        space_id, error = create_step(redis_cap, create_params, charge_params)
        assert error.code == 400
        assert error.status == "INVALID_ARGUMENT"
        info_logger.info("Test create master-slave instance with error charge duration successfully!")
