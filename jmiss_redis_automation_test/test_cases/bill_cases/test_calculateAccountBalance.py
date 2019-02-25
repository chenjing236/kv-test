from jmiss_redis_automation_test.steps.BillOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import *



class TestAccountBalance:

    instance_classes = [
        ("redis.m1.micro.basic", 60, 2.8),
        ("redis.m1.small.basic", 120, 2.8),
        # ("redis.m1.medium.basic", 240, 2.8),
        # ("redis.m1.large.basic", 480, 2.8),
        # ("redis.m1.xlarge.basic", 960, 2.8),
        # ("redis.m1.2xlarge.basic", 1920, 2.8),
        # ("redis.m1.4xlarge.basic", 3480, 2.8),
        # ("redis.c1.small.basic", 1440, 2.8),
        # ("redis.c1.medium.basic", 2880, 2.8),
        # ("redis.c1.large.basic", 5760, 2.8),
        # ("redis.c1.xlarge.basic", 11520, 2.8),
        # ("redis.c1.2xlarge.basic", 23040, 2.8),
        # ("redis.c1.4xlarge.basic", 46080, 2.8),
#######################  4.0
        # ("redis.m.micro.basic", 60, 4.0),
        # ("redis.m.small.basic", 120, 4.0),
        # ("redis.m.medium.basic", 240, 4.0),
        # ("redis.m.large.basic", 480, 4.0),
        # ("redis.m.xlarge.basic", 960, 4.0),
        # ("redis.m.2xlarge.basic", 1920, 4.0),
        # ("redis.m.4xlarge.basic", 3480, 4.0),
        # ("redis.c.small.basic", 1440, 4.0),
        # ("redis.c.medium.basic", 2880, 4.0),
        # ("redis.c.large.basic", 5760, 4.0),
        # ("redis.c.xlarge.basic", 11520, 4.0),
        # ("redis.c.2xlarge.basic", 23040, 4.0),
        # ("redis.c.4xlarge.basic", 46080, 4.0)
        ]

    @pytest.mark.bill
    @pytest.mark.parametrize('flavor, bill, redis_version', instance_classes)
    def test_calculateAccountBalance(self, config, flavor, bill, redis_version):
        url = "http://uc-inner-api-ite.jcloud.com/usercenter/getUser?pin=jcloudiaas2"
        before_account = get_account_balance(url, "stag")
        create_instance(config, flavor, "prepaid_by_duration", str(redis_version))
        time.sleep(3)
        after_account = get_account_balance(url, "stag")
        compare_balance(before_account, after_account, bill)





