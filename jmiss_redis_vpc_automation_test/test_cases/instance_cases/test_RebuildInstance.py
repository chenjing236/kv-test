# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestRebuildInstance:

    # @pytest.mark.rebuildinstance
    # def test_rebuild_repair_instance(self, config, created_instance, http_client):
    #     info_logger.info("[SCENARIO] Start to test rebuild repair instance")
    #     # 创建缓存云实例，创建成功
    #     info_logger.info("[STEP] Create an instance with a master container and a slave container")
    #     space_id, instance, password = created_instance
    #     info_logger.info("[INFO] The instance {0} is created".format(space_id))
    #     # 获取拓扑结构
    #     info_logger.info("[STEP2] Get topology information of instance {0}".format(space_id))
    #     masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
    #     info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
    #     info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
    #     # 通过master，执行set/get key
    #     # 执行rebuild流程（删除master和slave container，使资源状态变为101）
    #     info_logger.info("[STEP3] Start to run rebuild repair instance")
    #     cfs_client = CFS(config)
    #     container = Container(config, http_client)
    #     run_rebuild_repair_step(instance, space_id, container, cfs_client)
    #     info_logger.info("[STEP4] Get topology information of repaired instance {0}".format(space_id))
    #     masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
    #     info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
    #     info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
    #     # 通过AP访问缓存云实例，输入auth,可以正常访问
    #     # 通过AP访问获取key
    #     info_logger.info("[INFO] Test rebuild repair instance successfully!")

    @pytest.mark.rebuildinstance
    def test_rebuild_clone_instance(self, created_instance):
        info_logger.info("[SCENARIO] Start to test rebuild clone instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过master，执行set/get key
        info_logger.info("[INFO] It is successful to set key to the master of the instance {0}".format(space_id))
        # 执行clone操作
        info_logger.info("[STEP3] Start to run rebuild clone instance")
        space_id_clone = run_rebuild_clone_step(instance, space_id)
        info_logger.info("[STEP4] Check the flavor of the instance {0}".format(space_id))
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        detail_info_clone = get_detail_info_of_instance_step(instance, space_id_clone)
        assert detail_info_clone["status"] == 100, "[ERROR] The cluster status is not 100!"
        assert detail_info["flavorId"] == detail_info_clone["flavorId"], "[ERROR] The cluster flavor is wrong!"
        info_logger.info("[INFO] The flavor of cloned instance is same as old instance!")
        info_logger.info("[STEP5] Get topology information of cloned instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id_clone)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # 通过AP访问获取key
        # 删除clone的instance
        info_logger.info("[INFO] Delete the cloned instance")
        instance.delete_instance(space_id_clone)
        info_logger.info("[INFO] Test rebuild clone instance successfully!")

    @pytest.mark.rebuildinstance
    def test_rebuild_upgrade_instance(self, created_instance):
        info_logger.info("[SCENARIO] Start to test rebuild upgrade instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance {0} is created".format(space_id))
        # 获取拓扑结构
        info_logger.info("[STEP2] Get topology information of instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过master，执行set/get key
        info_logger.info("[INFO] It is successful to set key to the master of the instance {0}".format(space_id))
        # 执行upgrade操作
        info_logger.info("[STEP3] Start to run rebuild upgrade instance")
        run_rebuild_upgrade_step(instance, space_id)
        info_logger.info("[STEP4] Get topology information of upgraded instance {0}".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}: [{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}: [{1}]".format(slaveIp, slaveDocker))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # 通过AP访问获取key
        info_logger.info("[INFO] Test rebuild upgrade instance successfully!")
