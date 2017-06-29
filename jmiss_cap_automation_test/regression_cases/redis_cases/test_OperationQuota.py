# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestOperationQuota:

    @pytest.mark.smoke
    def test_operation_quota(self, config, instance_data, cap_http_client):
        info_logger.info("[INFO] Test modify operation quota!")
        #查询用户配额，如果total大于0，则total必须大于used
        resource ="redis"
        request_id, res_data_total, res_data_use = query_user_quota_step(config, instance_data, cap_http_client, resource)
        if res_data_total>0:
            assert res_data_total>res_data_use,"[INFO] Query user quota is incorrect,used quota > total quota"
        #调用中间层修改配额接口，将user_quota修改为total_quota，接口返回成功,user_quota大于total_quota时total_quota和user_quota相等。
        info_logger.info("[INFO] The total quota is {0}".format(res_data_total))
        info_logger.info("[INFO] The used quota is {0}".format(res_data_use))
        info_logger.info("[INFO] Start modify user quota to the max num")
        request_id, quota, use = modify_user_quota_step(config, instance_data, cap_http_client, resource, res_data_total)
        if quota>0:
            assert quota == use,"[INFO] Query user quota is incorrect,used quota !=  total quota"
        info_logger.info("[INFO] Modify user quota successfully, the used quota is {0} now".format(use))
        #调用中间层获取用户配额接口，调用接口成功，将user_quota修改成正常小于total_quota值
        info_logger.info("[INFO] Modify user quota back")
        request_id, quota, use = modify_user_quota_step(config, instance_data, cap_http_client, resource, res_data_use - res_data_total)
        if quota>0:
            assert quota >= use,"[INFO] Query user quota is incorrect,used quota !> total quota"
        info_logger.info("[INFO] Modify user quota successfully, the used quota is {0} now".format(use))
        info_logger.info("[INFO] Test operation quota successfully!")
