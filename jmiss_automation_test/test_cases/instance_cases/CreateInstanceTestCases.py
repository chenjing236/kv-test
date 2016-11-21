# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)

class CreateInstanceTestCases:
    #创建单实例缓存云实例，并验证数据库中的数据
    @pytest.mark.smoke
    def test_create_an_instance_using_db(self, config, instance_data, http_client):
        info_logger.info("[Scenario] It is successful to create an instance whith a master container and a slave container")
        #调用创建缓存云实例接口，创建单实例缓存云
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        #查询数据库表space表，查看缓存云实例的状态status=100
        space_id = create_instance_step(instance)

    @pytest.mark.smoke
    def F_test_topology_info_using_db(self):
        print "[Scenario] The information of topology for the instance is correct"
        info_logger.info("[Scenario] The information of topology for the instance is correct")
        #查看数据库topology表中拓扑结构
        #查看数据库instance表中拓扑结构
        #查看CFS的redis中的信息

    @pytest.mark.smoke
    def F_test_container_info(self):
        print "[Scenario] The information of containers for the instance is correct"
        info_logger.info("[Scenario] The information of containers for the instance is correct")
        #查看container信息，master continer是否是运行状态，且replication是master
        #查看container信息，master continer的大小
        #查看container信息，slave container是否是运行状态，且replication是slave
        #查看container信息，slave continer的大小

    #创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.smoke
    def F_test_create_an_instance_without_using_db(self):
        print "[Scenario] It is successful to create an instance whith a master container and a slave container."