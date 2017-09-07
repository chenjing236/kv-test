# -*- coding: utf-8 -*-

from BasicTestCase import *
from redis_stability_cases.ClearRemindedRedis import clear_reminded_redis

logger_info = logging.getLogger(__name__)

def main():
    conf_file = '../../config/redis_config/config_test.json'
    instance_file = '../../data/redis_data/data_test_with_new_payment.json'
    fd = open(conf_file, 'r')
    config = json.load(fd)
    fd.close()
    fd = open(instance_file, 'r')
    instance_data = json.load(fd)
    fd.close()
    redis_http_client = RedisCapClient(config["host"])
    cap_http_client = CapClient(config["host"])
    resource_id = ""
    redis_cap = RedisCap(config, instance_data, redis_http_client)
    cap = Cap(config, instance_data, cap_http_client)
    clear_reminded_redis(redis_cap, instance_data)




