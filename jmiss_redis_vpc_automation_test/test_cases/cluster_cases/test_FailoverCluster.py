# coding:utf-8
import random
from BasicTestCase import *

info_logger = logging.getLogger(__name__)


class TestFailoverCluster:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_master(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password, accesser = created_instance
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)
        # run master failover
        cfs_host = get_master_cfs_step(cluster)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("To stop the master container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["masterDocker"], container, cfs_client, 2)
        assert is_failover is True, info_logger.error("Run master failover is failed")
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        assert shards[failover_num]["masterDocker"] != shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] == shards_cfs[failover_num]["slaveDocker"]
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_slave(self, config, created_instance, http_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password, accesser = created_instance
        # 获取拓扑结构
        shards = get_topology_of_cluster_step(cluster, space_id)
        shard_count = len(shards)
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)
        # run slave failover
        cfs_host = get_master_cfs_step(cluster)
        cfs_client = CFS(cfs_host, config)
        container = Container(config, http_client)
        failover_num = random.randint(0, shard_count - 1)
        info_logger.info("To stop the slave container of shard_{0}".format(failover_num + 1))
        is_failover = run_failover_container_step(space_id, shards[failover_num]["slaveDocker"], container, cfs_client, 1)
        assert is_failover is True, info_logger.error("Run slave failover is failed")
        shards_cfs = get_topology_of_cluster_from_cfs_step(cfs_client, space_id)
        assert shards[failover_num]["masterDocker"] == shards_cfs[failover_num]["masterDocker"]
        assert shards[failover_num]["slaveDocker"] != shards_cfs[failover_num]["slaveDocker"]
        # 验证通过domain访问实例
        check_access_domain_step(accesser, space_id, password)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_failover_ap(self, config, created_instance, http_client, sql_client):
        # 创建缓存云实例，创建成功
        space_id, cluster, password, accesser = created_instance
        # 获取旧ap
        sql_str = "select docker_id,overlay_ip from ap where space_id='{0}'".format(space_id)
        docker_tuple = sql_client.exec_query_all(sql_str)
        docker_id = docker_tuple[0][0]
        # 删除ap
        container = Container(config, http_client)
        container.stop_jcs_docker(docker_id)
        # 等待failover
        sql_str = "select return_code FROM `scaler_task` WHERE space_id='{0}' \
                        and task_type=107 and task_id LIKE '{1}' order by id desc".format(space_id, "%" + docker_id)
        sql_client.wait_for_expectation(sql_str, 0, 5, 120)
        # 获取最新ap数据并进行验证
        sql_str = "select docker_id,overlay_ip from ap where space_id='{0}'".format(space_id)
        docker_tuple_new = sql_client.exec_query_all(sql_str)
        assert docker_tuple[1][1] == docker_tuple_new[0][1]
        assert len(docker_tuple) == len(docker_tuple_new)
        docker_list = [j for i in docker_tuple_new for j in i]
        assert docker_id not in docker_list
        check_access_domain_step(accesser, space_id, password)
