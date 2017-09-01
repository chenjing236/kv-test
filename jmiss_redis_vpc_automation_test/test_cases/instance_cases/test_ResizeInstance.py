# coding:utf-8
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestResizeInstance:

    @pytest.mark.resizeinstance
    def test_resize_instance(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to resize instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的flavor
        info_logger.info("[STEP2] Get the flavor of the origin instance %s", space_id)
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin instance is [{}]".format(flavor_id))
        # 执行扩容操作
        info_logger.info("[STEP3] Resize the instance %s", space_id)
        flavor_id_resize = instance_data["flavorIdResize"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_resize)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after resizing the instance {0}"\
            .format(space_id)
        assert flavor_id_new == flavor_id_resize, "[ERROR] The flavor is incorrect after resizing the instance {0}"\
            .format(space_id)
        assert status == 100, "[ERROR] The status of instance [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of instance %s after resize", space_id)
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp, slaveDocker))
        info_logger.info("[STEP5] Check the capacity of instance after resize")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master["total"] == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave["total"] == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to resize the instance [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # 通过AP访问获取key

    @pytest.mark.resizeinstance
    def test_reduce_instance(self, config, instance_data, created_instance, http_client):
        info_logger.info("[SCENARIO] Start to reduce instance")
        # 创建缓存云实例，创建成功
        info_logger.info("[STEP1] Create an instance with a master container and a slave container")
        space_id, instance, password = created_instance
        info_logger.info("[INFO] The instance %s is created", space_id)
        info_logger.info("[INFO] The password of instance {0} is {1}".format(space_id, password))
        # 获取原有缓存云实例的flavor
        info_logger.info("[STEP2] Get the memory size of the origin instance %s", space_id)
        detail_info = get_detail_info_of_instance_step(instance, space_id)
        flavor_id = detail_info["flavorId"]
        info_logger.info("[INFO] The flavorId of the origin instance is [{}]".format(flavor_id))
        # 执行缩容操作
        info_logger.info("[STEP3] Reduce the instance %s", space_id)
        flavor_id_reduce = instance_data["flavorIdReduce"]
        status, flavor_id_new = resize_instance_step(instance, space_id, flavor_id_reduce)
        # 验证扩容操作后的规格
        assert flavor_id_new != flavor_id, "[ERROR] The flavor is incorrect after reducing the instance {0}" \
            .format(space_id)
        assert flavor_id_new == flavor_id_reduce, "[ERROR] The flavor is incorrect after reducing the instance {0}" \
            .format(space_id)
        assert status == 100, "[ERROR] The status of instance [{0}] is not 100!".format(space_id)
        # 查询flavor对应的配置信息
        flavor = query_config_by_flavor_id_step(instance, flavor_id_new)
        capacity = flavor["memory"]
        # 获取拓扑结构
        info_logger.info("[STEP4] Get topology information of instance [{0}] after reduce".format(space_id))
        masterIp, masterDocker, slaveIp, slaveDocker = get_topology_of_instance_step(instance, space_id)
        info_logger.info("[INFO] Information of master container is {0}:[{1}]".format(masterIp, masterDocker))
        info_logger.info("[INFO] Information of slave container is {0}:[{1}]".format(slaveIp, slaveDocker))
        info_logger.info("[STEP5] Check the capacity of instance after reduce")
        container = Container(config, http_client)
        mem_info_master = get_container_info_step(container, masterIp, masterDocker)
        mem_info_slave = get_container_info_step(container, slaveIp, slaveDocker)
        assert mem_info_master["total"] == capacity, "[ERROR] Memory size of master container is inconsistent with request"
        assert mem_info_slave["total"] == capacity, "[ERROR] Memory size of slave container is inconsistent with request"
        info_logger.info("[INFO] It is successful to reduce the instance [{0}], the flavor is [{1}], "
                         "the capacity is [{2}]".format(space_id, flavor_id_new, capacity))
        # 通过AP访问缓存云实例，输入auth,可以正常访问
        # 通过AP访问获取key
