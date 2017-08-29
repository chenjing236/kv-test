# coding:utf-8
import pytest
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestCreateInstance:
    # 创建单实例缓存云实例，通过查询接口验证创建缓存云实例的正确性
    @pytest.mark.createInstance
    def test_create_instance(self, config, instance_data, http_client):
        info_logger.info("[SCENARIO] Create an instance including a master container and a slave container")
        instance = Cluster(config, instance_data, http_client)
        # 创建缓存云实例
        info_logger.info("[STEP1] Create an instance including a master container and a slave container")
        space_id, operation_id, password = create_instance_step(instance)
        info_logger.info("[INFO] The instance {0} is created, its password is {1}".format(space_id, password))
        # 查看创建操作结果，验证创建成功
        info_logger.info("[STEP2] Get creation result of the instance %s", space_id)
        is_success = get_operation_result_step(instance, space_id, operation_id)
        assert is_success is True, "[INFO] Get the right operation result, create instance successfully"
        # 查看redis详情，验证缓存云实例状态，status=100创建成功
        info_logger.info("[STEP3] Get detail info of the instance %s", space_id)
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        assert detail_info["status"] == 100, "[ERROR] The cluster status is not 100!"
        assert detail_info["zone"] != 'clsdocker', "[ERROR] The cluster zone is clsdocker!"
        info_logger.info("[INFO] Get the right detail info, the status of cluster {0} is 100".format(space_id))
        capacity = detail_info["capacity"]
        # 查看缓存云实例详情，获取拓扑结构
        info_logger.info("[STEP4] Get topology information of instance")
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp, slaveDocker))
        # 获取CFS的拓扑结构
        info_logger.info("[STEP5] Get topology information of instance from CFS")
        cfs_client = CFS(config)
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp_cfs, masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp_cfs, slaveDocker_cfs))
        assert masterIp == masterIp_cfs, "[ERROR] Ip of master container is inconsistent"
        assert masterDocker == masterDocker_cfs, "[ERROR] Docker_id of master container is inconsistent"
        assert slaveIp == slaveIp_cfs, "[ERROR] Ip of slave container is inconsistent"
        assert slaveDocker == slaveDocker_cfs, "[ERROR] Docker_id of slave container is inconsistent"
        # 获取container的大小，验证container的大小
        info_logger.info("[STEP6] Get container info from nova agent")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master["total"] == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave["total"] == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] Memory size of master and slave container is {0}".format(capacity))
        # 删除缓存云实例
        info_logger.info("[STEP7] Delete the instance {0}".format(space_id))
        delete_instance_step(instance, space_id)
