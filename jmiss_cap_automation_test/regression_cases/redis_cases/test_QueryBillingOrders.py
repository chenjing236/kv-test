# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestQueryBillingOrders:

    @pytest.mark.smoke
    def test_query_billing_orders(self, config, instance_data, cap_http_client):
        #创建主从版按配置redis资源
        condition = {"category":"0",
                     "feeType":0,
                     "resourceType":"redis" ,
                     "expireDays": -1,
                     "pageNumber": 1,
                     "pageSize":10,
                     "showRegion":"allRegion"}
        request_id, billingOrderTotal,billingOrders =  query_billing_orders_step(config, instance_data, cap_http_client, condition)
        print "++++"
        print billingOrderTotal
        print "-----"
        print billingOrders
        info_logger.info("[INFO] Test query billing orders successfully!")


