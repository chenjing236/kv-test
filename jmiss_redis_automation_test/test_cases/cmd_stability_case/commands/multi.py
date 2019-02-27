# coding=utf-8
import redis
import time
import random


# multi exec watch
def multi_exec_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】multi exec start, include [multi exec watch], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    # 清理测试数据
    for key in r.keys('*stab_multi*'):
        r.delete(key)
    for i in range(sec):
        # 写入测试数据
        for j in range(50):
            r.rpush('{stab_multi}list' + str(j), 'stab_multi_value' + str(j))
            r.set('{stab_multi}key' + str(j), 'stab_multi_value' + str(j))
        # watch
        watch_num = random.randint(0, 50)
        try:
            r.watch('{stab_multi}list' + str(watch_num))
            r.watch('{stab_multi}key' + str(watch_num))
        except Exception, err:
            print "【ERROR】DB {0} multi watch key error [{1}], i = {2}".format(db, err, i)
            continue
        # multi
        p = r.pipeline()
        for j in range(50):
            if j == watch_num:
                continue
            try:
                p.rpop('{stab_multi}list' + str(j))
                p.delete('{stab_multi}key' + str(j))
            except Exception, err:
                print "【ERROR】DB {0} multi rpop/del error [{1}], i = {2}".format(db, err, i)
                continue
            time.sleep(0.01)
        try:
            p.execute()
        except Exception, err:
            print "【ERROR】DB {0} multi exec error [{1}]".format(db, err)
            continue
        if r.rpop('{stab_multi}list' + str(watch_num)) != 'stab_multi_value' + str(watch_num):
            print "【ERROR】DB {0} multi watched list {{stab_multi}}list{1} is changed!".format(db, watch_num)
        if r.get('{stab_multi}key' + str(watch_num)) != 'stab_multi_value' + str(watch_num):
            print "【ERROR】DB {0} multi watched key {{stab_multi}}key{1} is changed!".format(db, watch_num)
        r.delete('{stab_multi}key' + str(watch_num))
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】multi exec end, db number is {0}, run time is {1} sec".format(db, sec)


# multi discard watch unwatch
def multi_discard_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】scan keys start, include [scan], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    # 清理数据
    for key in r.keys('stab_scan_key*'):
        r.delete(key)
    for i in range(sec):
        # 写入测试数据
        for j in range(1000):
            r.set('stab_scan_key' + str(j), 'scan_value' + str(j))
            # time.sleep(0.01)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】scan keys end, db number is {0}, run time is {1} sec".format(db, sec)


# multi exec watch
