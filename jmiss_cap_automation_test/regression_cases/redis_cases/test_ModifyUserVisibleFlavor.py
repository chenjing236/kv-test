# -*- coding: utf-8 -*- 

from BasicTestCase import *
from steps.RedisClusterOperationSteps import *


class TestModifyUserVisibleFlavor:

    @pytest.mark.smoke
    def test_modify_user_visible_flavor(self, config, instance_data, redis_http_client, cap_http_client):
        info_logger.info("[Scenario] Test modify user visible flavor!")
        redis_cap = RedisCap(config, instance_data, redis_http_client)
        cap = Cap(config, instance_data, cap_http_client)
        #调用中间层查询flavor接口查询用户可见flavor列表，正确返回用户flavor列表
        request_id, flavors = query_flavors_step(redis_cap)
        is_512_canSee = False
        for flavor in flavors:
            if flavor["memory"] == 524288:
                is_512_canSee = True
        cpu = "32"
        memory = "512"
        disk = "0"
        if is_512_canSee is True:
            info_logger.info("[INFO] The 512 flavor is already exist, delete it now")
            action_type = -1
            modify_user_visible_flavor_step(redis_cap, cpu, memory, disk, action_type)
            request_id, flavors = query_flavors_step(redis_cap)
            is_512_canSee = False
            for flavor in flavors:
                if flavor["memory"] == 524288:
                    is_512_canSee = True
        assert is_512_canSee is False, "[Info] Before set flavor is not OK"
        info_logger.info("[INFO] Before set flavor, the 512 flavor is not exist")
        time.sleep(3)
        #调用中间层运营接口给用户添加512G集群的flavor，接口返回成功
        #action_type
        #1:flavor可见
        #0:该条flavor设置失效
        #-1:flavor不可见
        action_type = 1
        modify_user_visible_flavor_step(redis_cap, cpu, memory, disk, action_type)
        #调用中间层查询flavor接口，接口调用成功，返回flavor列表中存在512G的flavor
        request_id, flavors = query_flavors_step(redis_cap)
        is_512_canSee = False
        for flavor in flavors:
            print flavor
            if flavor["memory"] ==524288:
                is_512_canSee = True

        assert is_512_canSee == True ,"[Info] Before set flavor is not OK "
        #调用中间层运营接口删除用户512G集群的flavor，接口返回成功
        action_type = -1
        modify_user_visible_flavor_step(redis_cap, cpu, memory, disk, action_type)
        #调用中间层查询flavor接口，接口调用成功，返回flavor列表中没有512G的flavor
        request_id, flavors =query_flavors_step(redis_cap)
        is_512_canSee = False
        for flavor in flavors:
            if flavor["memory"] ==524288:
                is_512_canSee = True

        assert is_512_canSee == False ,"[Info] After set flavor is not OK "
        info_logger.info("[INFO] Test modify user visible flavor successfully!")

