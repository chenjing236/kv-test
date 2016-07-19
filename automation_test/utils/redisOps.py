import redis
import time
import json

def check_redis_instances(instances):
    master = instances[0]
    slave = instances[1]

    cnt = redis.StrictRedis(host=master[0], port=master[1])
    cnt.set("test", "test_str")
    assert cnt.get("test") == "test_str"
    time.sleep(1)
    cnt_slave = redis.StrictRedis(host=slave[0], port=slave[1])
    assert cnt_slave.get("test") == "test_str"
    cnt.delete('test')
    assert cnt_slave.get("test") is None

def get_value(redisInfo,key):
    cnt_redis = redis.StrictRedis(host=redisInfo[0], port=redisInfo[1])
    time.sleep(1)
    return cnt_redis.get(key)

def set_key_value(master,key,value):
    cnt = redis.StrictRedis(host=master[0], port=master[1])
    cnt.set(key, value)
    time.sleep(1)

def delete_key_value(master,key):
    cnt = redis.StrictRedis(host=master[0], port=master[1])
    cnt.delete(key)
    time.sleep(1)

def check_ap_access(ap_host, ap_port, passwd, jinstance):
    cnt = redis.StrictRedis(host=ap_host, port=ap_port, password=passwd)
    cnt.set("test_ap", "test_ap_value")
    assert cnt.get("test_ap") == "test_ap_value"

    cnt_ins = redis.StrictRedis(host=jinstance[0], port=jinstance[1])
    assert cnt_ins.get("test_ap") == "test_ap_value"

def get_redis_info(redis_host, redis_port):
    cnt = redis.StrictRedis(host=redis_host, port=redis_port)
    info = cnt.info()
    if len(info) < 1:
        raise Exception("[ERROR] Cannot get information for redis({0}:{1})").format(redis_host,redis_port)

    redis_info = json.loads(json.dumps(info).replace("'","\""))
    return redis_info