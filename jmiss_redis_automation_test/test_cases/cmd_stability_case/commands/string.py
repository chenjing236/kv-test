# coding=utf-8
import redis
import time


# set get del
def set_keys(host, port, db, password, sec):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【START】string test start, include [set get del], db number is {0}, run time is {1} sec".format(db, sec)
    r = redis.Redis(host=host, port=port, db=db, password=password)
    for i in range(sec * 50):
        # set
        r.set('stab_set_keys' + str(i), 'set_value' + str(i))
        # get
        if r.get('stab_set_keys' + str(i)) != 'set_value' + str(i):
            print "【ERROR】DB {0} get key [stab_set_keys{1}] is not equal value [set_value{2}]".format(db, i, i)
        time.sleep(0.01)
    for i in range(sec * 50):
        # del
        r.delete('stab_set_keys' + str(i))
        time.sleep(0.01)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), " - 【END】string test end, db number is {0}, run time is {1} sec".format(db, sec)
