# coding:utf-8
from BasicTestCase import *


class TestModifyClusterConfig:
    @pytest.mark.test
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_modify_instance_config(self, config, created_instance):
        # 创建缓存云实例，创建成功
        space_id, instance, password, accesser = created_instance
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)
        # todo: 查看当前instance config
        # 执行修改自定义参数
        modify_instance_config_step(instance, space_id, {"hash-max-ziplist-value": "138",
                                                         "hash-max-ziplist-entries": "522",
                                                         "list-max-ziplist-entries": "510",
                                                         "list-max-ziplist-value": "110"})
        # 查询详情接口，验证资源状态正确
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        assert detail_info["status"] == 100, info_logger.error("The status of space [{0}] is wrong after modify config!".format(space_id))
        # todo: 查看修改后的instance config
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)
