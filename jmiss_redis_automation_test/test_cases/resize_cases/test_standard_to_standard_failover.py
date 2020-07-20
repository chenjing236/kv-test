#!/bin/python
# coding:utf-8
import threading
import uuid
from time import sleep

import pytest

from jmiss_redis_automation_test.steps.FailoverOperation import trigger_docker_failover
from jmiss_redis_automation_test.steps.FusionOpertation import reset_class, send_web_command
from jmiss_redis_automation_test.steps.InstanceOperation import create_validate_instance, wait_docker_run_time_change
from jmiss_redis_automation_test.steps.Valification import assertRespNotNone
from jmiss_redis_automation_test.steps.WebCommand import WebCommand
from jmiss_redis_automation_test.steps.WriteData import write_data
from jmiss_redis_automation_test.steps.base_test.MultiCheck import check_admin_proxy_redis_configmap, \
    get_docker_running_time
from jmiss_redis_automation_test.steps.base_test.admin import get_current_rs_type, get_space_status, get_next_rs_type
from jmiss_redis_automation_test.steps.base_test.baseCheckPoint import baseCheckPoint
from jmiss_redis_automation_test.steps.base_test.configmap import get_job
from jmiss_redis_automation_test.steps.base_test.proxy import get_proxy_num
from jmiss_redis_automation_test.steps.base_test.redis import get_redis_num
from jmiss_redis_automation_test.utils.util import get_shard_id


class TestStandardToStandardFailover:
    # 1个源端master failover
    def test_source_master_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num=instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client,shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],instance["instance_password"])
        expected_object.side=1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"

        # 等待resize开始
        for i in range(0,600):
            resp_get_job=get_job(instanceId,config,str(resp.request_id))
            if resp_get_job["code"]==0:
                break
            sleep(1)

        # 触发master failover
        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status=trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config,instanceId,oldRunTime,replicasetName,dockerName)

        # 手动调用任务恢复接口
        print(
            "please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0,3600):
            if get_space_status(instanceId,config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId,config,expected_object,shard_num)

    # 1个源端slave failover
    def test_source_slave_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],instance["instance_password"])
        expected_object.side=1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"


        # 等待resize开始
        for i in range(0,600):
            resp_get_job=get_job(instanceId,config,str(resp.request_id))
            if resp_get_job["code"]==0:
                break
            sleep(1)

        # 触发slave failover
        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instanceId, config["region"], docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        # 手动调用任务恢复接口
        print(
            "please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0,3600):
            if get_space_status(instanceId,config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId,config,expected_object,shard_num)
    # 1个proxy failover
    def test_proxy_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],instance["instance_password"])
        expected_object.side=1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"


        # 等待resize开始
        for i in range(0,600):
            resp_get_job=get_job(instanceId,config,str(resp.request_id))
            if resp_get_job["code"]==0:
                break
            sleep(1)

        # 触发proxy failover
        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        replicasetName = instanceId + "-proxy"
        dockerName = replicasetName + "-" + str(proxyId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status=trigger_docker_failover("proxy",config,instanceId,config["region"],id=proxyId)
        assert status == 200

        assert wait_docker_run_time_change(config,instanceId,oldRunTime,replicasetName,dockerName)
        print(
            "please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0,3600):
            if get_space_status(instanceId,config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId,config,expected_object,shard_num)

    # 1个目的端master failover
    def test_target_master_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],instance["instance_password"])
        expected_object.side=1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"


        # 等待spaceStatus变为DoingCopyfrom
        for i in range(0,1200):
            resp_status=get_space_status(instanceId,config)
            if resp_status=="DoingCopyfrom":
                break
            sleep(1)

        # 触发master failover
        next_rs_type = get_next_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, next_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + next_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("redis",config,instanceId,config["region"],docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        # 手动调用任务恢复接口
        print("please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0,3600):
            if get_space_status(instanceId,config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId,config,expected_object,shard_num)


    # 1个目的端slave failover
    def test_target_slave_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],instance["instance_password"])
        expected_object.side=1
        expected_object.current_rs_type="b"
        expected_object.next_rs_type="a"


        # 等待spaceStatus变为DoingCopyfrom
        for i in range(0,1200):
            resp_status=get_space_status(instanceId,config)
            if resp_status=="DoingCopyfrom":
                break
            sleep(1)

        # 触发slave failover
        next_rs_type = get_next_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config,next_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-slave-" + next_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instanceId, config["region"], docker_name=dockerName)
        assert status == 200

        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        # 手动调用任务恢复接口
        print("please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0,3600):
            if get_space_status(instanceId,config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId,config,expected_object,shard_num)


    # 1个proxy和1个源端master failover
    def test_source_master_and_proxy_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]], instance["instance_password"])
        expected_object.side = 1
        expected_object.current_rs_type = "b"
        expected_object.next_rs_type = "a"

        # 等待resize开始
        for i in range(0, 600):
            resp_get_job = get_job(instanceId, config, str(resp.request_id))
            if resp_get_job["code"] == 0:
                break
            sleep(1)

        # 触发master failover
        current_rs_type = get_current_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, current_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + current_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instanceId, config["region"], docker_name=dockerName)
        assert status == 200

        # 触发proxy failover
        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        proxyReplicasetName = instanceId + "-proxy"
        proxyDockerName = proxyReplicasetName + "-" + str(proxyId)
        proxyOldRunTime = get_docker_running_time(config, instanceId, proxyReplicasetName, proxyDockerName)
        status = trigger_docker_failover("proxy", config, instanceId, config["region"],id=proxyId)
        assert status == 200

        # 等待redis failover结束
        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        #等待proxy failover结束
        assert wait_docker_run_time_change(config, instanceId, proxyOldRunTime, proxyReplicasetName, proxyDockerName)

        # 手动调用任务恢复接口
        print("please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0, 3600):
            if get_space_status(instanceId, config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, shard_num)

    # 1个proxy和1个目的端master failover
    def test_target_master_and_proxy_failover(self, config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]

        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        shard_num = instance["target_shardNumber"]
        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client, shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]], instance["instance_password"])
        expected_object.side = 1
        expected_object.current_rs_type = "b"
        expected_object.next_rs_type = "a"

        # 等待spaceStatus变为DoingCopyfrom
        for i in range(0, 1200):
            resp_status = get_space_status(instanceId, config)
            if resp_status == "DoingCopyfrom":
                break
            sleep(1)

        # 触发master failover
        next_rs_type = get_next_rs_type(instanceId, config)
        redisNum = get_redis_num(instanceId, config, next_rs_type)
        redisId = get_shard_id(redisNum, 1)[0]
        replicasetName = instanceId + "-master-" + next_rs_type
        dockerName = replicasetName + "-" + str(redisId)
        oldRunTime = get_docker_running_time(config, instanceId, replicasetName, dockerName)
        status = trigger_docker_failover("redis", config, instanceId, config["region"], docker_name=dockerName)
        assert status == 200

        # 触发proxy failover
        proxyId = get_shard_id(get_proxy_num(instanceId, config), 1)[0]
        proxyReplicasetName = instanceId + "-proxy"
        proxyDockerName = proxyReplicasetName + "-" + str(proxyId)
        proxyOldRunTime = get_docker_running_time(config, instanceId, proxyReplicasetName, proxyDockerName)
        status = trigger_docker_failover("proxy", config, instanceId, config["region"],id=proxyId)
        assert status == 200

        # 等待redis failover结束
        assert wait_docker_run_time_change(config, instanceId, oldRunTime, replicasetName, dockerName)

        #等待proxy failover结束
        assert wait_docker_run_time_change(config, instanceId, proxyOldRunTime, proxyReplicasetName, proxyDockerName)

        # 手动调用任务恢复接口
        print("please run recover task interface.For example:curl http://127.0.0.1:1818/reloadTask -d '{\"taskId\":\"$taskId\",\"isRollback\":false}'")

        sleep(10)
        for i in range(0, 3600):
            if get_space_status(instanceId, config) == "Running":
                break
            sleep(1)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, shard_num)

    #变配过程中测试所有的命令
    def test_all_command(self,config, instance_data, expected_data):
        instance = instance_data["modify_standard_instance"]
    
        expected_object = baseCheckPoint(expected_data[instance["cacheInstanceClass"]],
                                         instance["instance_password"])
        client, _, instanceId = create_validate_instance(config, instance, expected_object)

        write_data(config,instanceId,1024*1024*1024*0.8,instance["instance_password"])

        shard_num = instance["target_shardNumber"]

        resp = reset_class(config, instanceId, instance["target_cacheInstanceClass"], client=None, shardNumber=shard_num)
        assertRespNotNone(resp)

        expected_object = baseCheckPoint(expected_data[instance["target_cacheInstanceClass"]],
                                         instance["instance_password"])
        expected_object.side = 1
        expected_object.current_rs_type = "b"
        expected_object.next_rs_type = "a"

        # 等待spaceStatus变为DoingCopyfrom
        '''
        for i in range(0, 1200):
            resp_status = get_space_status(instanceId, config)
            if resp_status == "DoingCopyfrom":
                break
            sleep(1)
        '''
        resp = send_web_command(config, instanceId, config["region"], "auth " + instance["instance_password"])
        token = resp.result["token"]
        object = WebCommand(config, instanceId, config["region"], token)

        threading.Thread(target=send_web_command,args=(config,instanceId,config["region"],"blpop " + str(uuid.uuid1())+" 300", None,token))
        #t = threading.Thread(target=object.runAllForeverCommand())
        #t.setDaemon(True)
        #t.start()

        sleep(10)
        for i in range(0, 3600):
            if get_space_status(instanceId, config) == "Running":
                break
            sleep(1)

        #t.join(10)

        assert check_admin_proxy_redis_configmap(instanceId, config, expected_object, shard_num)







