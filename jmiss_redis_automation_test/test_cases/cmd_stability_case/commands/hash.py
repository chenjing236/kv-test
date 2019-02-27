# coding=utf-8
import redis
import time


# hset hget hlen
def hset_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】hset test start, include [hset hget hlen], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec):
        r.delete('stab_hset_hash' + str(i))
        # hset
        for j in range(50):
            r.hset('stab_hset_hash' + str(i), 'hset_key' + str(j), 'hset_value' + str(j))
            time.sleep(0.01)
        # hlen
        if r.hlen('stab_hset_hash' + str(i)) != 50:
            print "【ERROR】DB {0} hlen hash [stab_hset_hash{1}] is not equal 50!".format(db, i)
        # hget
        for j in range(50):
            if r.hget('stab_hset_hash' + str(i), 'hset_key' + str(j)) != 'hset_value' + str(j):
                print "【ERROR】DB {0} hget hash [stab_hset_hash{1} | hset_key{2}] is not equal value pattern [hset_value{3}]".format(db, i, j, j)
            time.sleep(0.01)
    # 清理数据
    for i in range(sec):
        r.delete('stab_hset_hash' + str(i))
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】set test end, db number is {0}, run time is {1} sec".format(db, sec)
