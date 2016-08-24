import redis
import time


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


def check_ap_access(ap_host, ap_port, passwd, jinstance):
    cnt = redis.StrictRedis(host=ap_host, port=ap_port, password=passwd)
    cnt.set("test_ap", "test_ap_value")
    assert cnt.get("test_ap") == "test_ap_value"

    cnt_ins = redis.StrictRedis(host=jinstance[0], port=jinstance[1])
    assert cnt_ins.get("test_ap") == "test_ap_value"
