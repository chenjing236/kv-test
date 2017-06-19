# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestOperationQuota:

    @pytest.mark.smoke
    def test_operation_quota(self, create_redis_instance,config,instance_data ,cap_http_client):
        #查询用户配额，如果total大于0，则total必须大于used
        resource ="redis"
        request_id, res_data_total, res_data_use = query_user_quota_step(config, instance_data, cap_http_client, resource)
        if res_data_total>0:
            assert res_data_total>res_data_use,"[INFO] Query user quota is incorrect,used quota > tatal quota"
        #调用中间层修改配额接口，将user_quota修改为total_quota，接口返回成功,user_quota大于total_quota时total_quota和user_quota相等。
        print "======"
        print res_data_total
        print res_data_use
        request_id, quota, use = modify_user_quota_step(config, instance_data, cap_http_client, resource, res_data_total)
        if quota>0:
            assert quota == use,"[INFO] Query user quota is incorrect,used quota !=  tatal quota"
        #调用中间层获取用户配额接口，调用接口成功，将user_quota修改成正常小于total_quota值
        request_id, quota, use = modify_user_quota_step(config, instance_data, cap_http_client, resource, -7)
        if quota>0:
            assert quota > use,"[INFO] Query user quota is incorrect,used quota !> tatal quota"

        info_logger.info("[INFO] Test operation quota successfully!")
