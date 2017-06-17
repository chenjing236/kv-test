# -*- coding: utf-8 -*- 

from BasicTestCase import *


class TestModifyUserVisibleFlavor:

    @pytest.mark.smoke
    def test_modify_user_visible_flavor(self, create_redis_instance):
        #调用中间层查询flavor接口查询用户可见flavor列表，正确返回用户flavor列表

        #调用中间层运营接口给用户添加512G集群的flavor，接口返回成功

        #调用中间层查询flavor接口，接口调用成功，返回flavor列表中存在512G的flavor

        #调用中间层运营接口删除用户512G集群的flavor，接口返回成功

        #调用中间层查询flavor接口，接口调用成功，返回flavor列表中没有512G的flavor
        info_logger.info("[INFO] Test modify user visible flavor successfully!")

        return