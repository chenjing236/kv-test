# coding:utf-8

from BasicTestCase import *

info_logger = logging.getLogger(__name__)


# todo：ap failover
class TestFailoverCluster:
    @pytest.mark.smoke
    def test_failover_master(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to run failover master")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the instance {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，执行set/get key
        # run master failover
        info_logger.info("[STEP3] Run failover for master container")
        cfs_client = CFS(config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, masterDocker, container, cfs_client, 2)
        assert is_failover is True, "[ERROR] Run master failover is failed"
        logger_info.info("[INFO] It is successful to run master failover")
        info_logger.info("[STEP4] Get topology information from CFS {0}".format(space_id))
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(cfs_client, space_id)
        info_logger.info("[INFO] Information of master container after master failover is {0}: [{1}]".format(masterIp_cfs, masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container after master failover is {0}: [{1}]".format(slaveIp_cfs, slaveDocker_cfs))
        assert masterDocker != masterDocker_cfs
        assert slaveDocker == slaveDocker_cfs
        info_logger.info("[INFO] Test master failover successfully!")
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # 通过AP访问获取key
        # 通过AP访问缓存云实例，执行set/get key

    @pytest.mark.smoke
    def test_failover_slave(self, config, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to run failover slave")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        info_logger.info("[INFO] The password of the instance {0} is {1}".format(space_id, password))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of the instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，执行set/get key
        # run master failover
        info_logger.info("[STEP3] Run failover for slave container")
        cfs_client = CFS(config)
        container = Container(config, http_client)
        is_failover = run_failover_container_step(space_id, slaveDocker, container, cfs_client, 1)
        assert is_failover is True, "[ERROR] Run slave failover is failed"
        logger_info.info("[INFO] It is successful to run slave failover")
        masterIp_cfs, masterDocker_cfs, slaveIp_cfs, slaveDocker_cfs = get_topology_of_instance_from_cfs_step(
            cfs_client, space_id)
        info_logger.info("[INFO] Information of master container after slave failover is {0}: [{1}]".format(masterIp_cfs, masterDocker_cfs))
        info_logger.info("[INFO] Information of slave container after slave failover is {0}: [{1}]".format(slaveIp_cfs, slaveDocker_cfs))
        assert masterDocker == masterDocker_cfs
        assert slaveDocker != slaveDocker_cfs
        info_logger.info("[INFO] Test slave failover successfully!")
