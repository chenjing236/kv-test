# code = utf-8
import redis
import time

redis_client = redis.Redis(host="redis-c90vobttdm.cn-north-1.redis.jdcloud.com", port=6379)
exec_times = 1000000
quit_times = 50
exec_times += quit_times
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

for i in range(quit_times):
    for j in range(exec_times / quit_times):
        get_result = redis_client.get("test_rand_key")
    quit_result = redis_client.connection_pool.disconnect()
# for i in range(exec_times):
#     get_result = redis_client.get("test_rand_key")
#     print get_result
