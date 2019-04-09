# coding=utf-8
import redis
import time


# lpush lpop llen
def lpush_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】list test start, include [lpush lpop llen], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec):
        r.delete('stab_lpush_list' + str(i))
        # lpush
        for j in range(50):
            r.lpush('stab_lpush_list' + str(i), 'lpush_value' + str(j))
            time.sleep(0.01)
        # llen
        if r.llen('stab_lpush_list' + str(i)) != 50:
            print "【ERROR】DB {0} llen list [stab_lpush_list{1}] is not equal 50!".format(db, i)
        # lpop
        for j in range(50):
            if r.lpop('stab_lpush_list' + str(i)) != 'lpush_value' + str(49 - j):
                print "【ERROR】DB {0} lpop list [stab_lpush_list{1}] is not equal value [lpush_value{2}]".format(db, i, 49 - j)
            time.sleep(0.01)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】list test end, db number is {0}, run time is {1} sec".format(db, sec)


# rpush rpop llen
def rpush_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】list test start, include [rpush rpop llen], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec):
        r.delete('stab_rpush_list' + str(i))
        # rpush
        for j in range(50):
            r.rpush('stab_rpush_list' + str(i), 'rpush_value' + str(49 - j))
            time.sleep(0.01)
        # llen
        if r.llen('stab_rpush_list' + str(i)) != 50:
            print "【ERROR】DB {0} llen list [stab_rpush_list{1}] is not equal 50!".format(db, i)
        # rpop
        for j in range(50):
            if r.rpop('stab_rpush_list' + str(i)) != 'rpush_value' + str(j):
                print "【ERROR】DB {0} rpop list [stab_rpush_list{1}] is not equal value [rpush_value{2}]".format(db, i, j)
            time.sleep(0.01)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】list test end, db number is {0}, run time is {1} sec".format(db, sec)
