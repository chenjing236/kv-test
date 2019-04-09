# coding=utf-8
import redis
import time


# scan
def scan_keys(host, port, db, password, sec):
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
        scan_cursor = 0
        scan_len = 0
        while True:
            (scan_cursor, scan_key) = r.scan(cursor=scan_cursor, match='stab_scan_key*', count=10000)
            scan_len += len(scan_key)
            time.sleep(0.01)
            if scan_cursor == 0:
                break
        # 验证scan总数正确
        if scan_len != 1000:
            print "【ERROR】DB {0} scan keys num [stab_scan_key.len={1}] is not equal 1000!".format(db, scan_len)
    # 清理数据
    for j in range(1000):
        r.delete('stab_scan_key' + str(j))
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】scan keys end, db number is {0}, run time is {1} sec".format(db, sec)
