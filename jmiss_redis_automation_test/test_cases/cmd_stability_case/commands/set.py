# coding=utf-8
import redis
import time
import re


# sadd spop scard
def sadd_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】set test start, include [sadd spop scard], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec):
        r.delete('stab_sadd_set' + str(i))
        # sadd
        for j in range(50):
            r.sadd('stab_sadd_set' + str(i), 'sadd_value' + str(j))
            time.sleep(0.01)
        # scard
        if r.scard('stab_sadd_set' + str(i)) != 50:
            print "【ERROR】DB {0} scard set [stab_sadd_set{1}] is not equal 50!".format(db, i)
        # spop
        for j in range(50):
            if re.match('sadd_value', r.spop('stab_sadd_set' + str(i))) is None:
                print "【ERROR】DB {0} spop set [stab_sadd_set{1}] is not equal value pattern [sadd_value+num]".format(db, i)
            time.sleep(0.01)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】set test end, db number is {0}, run time is {1} sec".format(db, sec)


def zadd_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】set test start, include [zadd zrange scard], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec):
        r.delete('stab_zadd_set' + str(i))
        # zadd
        for j in range(50):
            r.zadd('stab_zadd_set' + str(i), dict([('zadd_value' + str(j), j)]))
            time.sleep(0.01)
        # zcard
        if r.zcard('stab_zadd_set' + str(i)) != 50:
            print "【ERROR】DB {0} zcard set [stab_zadd_set{1}] is not equal 50!".format(db, i)
        # zrange
        for j in range(50):
            if r.zrange('stab_zadd_set' + str(i), j, j)[0] != 'zadd_value' + str(j):
                print "【ERROR】DB {0} zrange set [stab_zadd_set{1}] is not equal value [zadd_value{2}]".format(db, i, j)
            time.sleep(0.01)
    # 清理数据
    for i in range(sec):
        r.delete('stab_zadd_set' + str(i))
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】set test end, db number is {0}, run time is {1} sec".format(db, sec)
