# coding:utf-8
import time
from business_function.Cluster import *


# upgrade cluster ap
def upgrade_ap_step(instance, space_id):
    print "\n"
    print "[STEP] Upgrade proxy of cluster [{0}]".format(space_id)
    res_data = instance.upgrade_instance_ap(space_id, instance.conf_obj["ap_image_tag"])
    code = res_data["Code"]
    msg = json.dumps(res_data["Message"], ensure_ascii=False).encode("gbk")
    assert code == 0, "It is failed to upgrade cluster proxy, error message is {0}".format(msg)
    return space_id


# upgrade cluster ap
def upgrade_redis_step(instance, space_id):
    print "\n"
    print "[STEP] Upgrade redis of cluster [{0}]".format(space_id)
    res_data = instance.upgrade_instance_ap(space_id, instance.conf_obj["redis_image_tag"])
    code = res_data["Code"]
    msg = json.dumps(res_data["Message"], ensure_ascii=False).encode("gbk")
    assert code == 0, "It is failed to upgrade cluster redis, error message is {0}".format(msg)
    return space_id


def get_operation_result_step(instance, space_id):
    # 获取操作结果，判断对资源的操作是否成功
    print "[STEP] Get creation result of the instance {0}".format(space_id)
    return_code = 1
    status = 0
    count = 1
    retry_times = instance.conf_obj["retry_times"]
    wait_time = instance.conf_obj["wait_time"]
    while return_code == 1 and count < retry_times:
        task_tuple = instance.sqlClient.exec_query_one("select task_id, status, return_code, message from scaler_task "
                                                     "where space_id = '{0}' and task_type = 110 "
                                                     "order by id desc".format(space_id))
        # task_id = task_tuple[0][0]
        status = int(task_tuple[1])
        return_code = int(task_tuple[2])
        message = task_tuple[3]
        print "Task query [{0} times] getting operation result is [{1}], status is [{2}]".format(count, message, status)
        count += 1
        time.sleep(wait_time)
    if count >= retry_times:
        assert False, "The operation of instance is failed"
    assert status == 14 and return_code == 0
    print "Get the right operation result, Task exec successfully"
    return True
