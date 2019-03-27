from jmiss_redis_automation_test.steps.BillOperation import *
from jmiss_redis_automation_test.steps.InstanceOperation import *



class TestAccountBalance:



    @pytest.mark.bill
    def test_accountBalance(self, init_instance, config):
        client, resp, instance_id = init_instance
        after_account = get_account_balance(str(config["uc_url"]), str(config["uc_token"]))
        compare_balance(config["before_account"], after_account, 60)








