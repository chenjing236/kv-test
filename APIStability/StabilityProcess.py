from multiprocessing import Process, Lock
from Queue import Queue
import sys

sys.path.append("../automation_test/")
from utils.JCacheUtils import *
from utils.WebClient import *
from utils.SQLClient import SQLClient
import random
import time
import os
import json


class Counter():
    def __init__(self, max_count):
        self.locker = Lock()
        self.count = 0
        self.max_count = max_count

    def check(self):
        res = True
        self.locker.acquire()
        self.count += 1
        if self.count >= self.max_count:
            res = False
        self.locker.release()
        return res


class JcacheAPIProcess(Process):
    def __init__(self, conf, res_queue, counter):
        super(JcacheAPIProcess, self).__init__()
        self.conf = conf
        self.min_cap = conf['min_cap']
        self.max_cap = conf['max_cap']
        self.max_sleep_time = conf['max_sleep_time']
        self.res_queue = res_queue
        self.counter = counter

    def get_cap(self):
        random.seed(int(time.time()))
        cap = random.randint(self.min_cap, self.max_cap) * 1024 * 1024
        return cap

    def run(self):
        wc = WebClient(self.conf['host'], self.conf['md5_pin'], self.conf['auth_token'])
        sql_c = SQLClient(self.conf['db_host'], self.conf['db_port'], self.conf['db_user'], self.conf['db_password'],
                          self.conf['db_name'])
        idx = 0
        while True:
            if not self.counter.check():
                self.res_queue.put(None)
                break

            pid = os.getpid()
            remarks = "remarks_{0}_{1}".format(pid, idx)
            name = "name_{0}_{1}".format(pid, idx)
            ca = CreateArgs(capacity=self.get_cap(), remarks=remarks, space_name=name)

            status, space_id = CreateCluster(wc, ca, sql_c)
            if status != 0:
                if space_id is not None:
                    DeleteCluster(wc, space_id, sql_c)
                self.res_queue.put((False, None, None))
                continue

            # check acl
            result = SetAcl(wc, space_id, sql_c, ["192.168.169.51", "192.168.169.87"])
            acl_check = True
            if result != 0:
                acl_check = False

            sleep_time = random.randint(0, self.max_sleep_time)
            time.sleep(sleep_time * 60)

            # check delete
            status, space_id = DeleteCluster(wc, space_id, sql_c)
            if status != 0:
                DeleteCluster(wc, space_id, sql_c)
                self.res_queue.put((True, acl_check, False))
                continue
            self.res_queue.put(True, acl_check, True)


class Stat(object):
    def __init__(self):
        self.total_num = 0
        self.fail_num = 0

    def add(self, success):
        if not success:
            self.fail_num += 1
        self.total_num += 1

    def get_stat(self):
        error_rate = 0.0
        if self.total_num != 0:
            error_rate = float(self.fail_num) / self.total_num
        return self.fail_num, self.total_num, error_rate

    def to_string(self):
        fn, tn, fr = self.get_stat()
        return "fail_num:{0}, total_num:{1}, error_rate:{2}".format(fn, tn, fr)


class statProcess(Process):
    def __init__(self, result_queue, producer_num):
        super(statProcess, self).__init__()
        self.result_queue = result_queue
        self.producer_num = producer_num

    def run(self):
        create_stat = Stat()
        acl_stat = Stat()
        delete_stat = Stat()
        exit_producer_num = 0
        while True:
            res = self.result_queue.get()
            if res is not None:
                create_res, acl_res, delete_res = res
                if create_res is not None:
                    create_stat.add(create_res)
                if acl_res is not None:
                    acl_stat.add(acl_res)
                if delete_res is not None:
                    delete_stat.add(delete_res)
            else:
                exit_producer_num += 1
                if exit_producer_num >= self.producer_num:
                    print "process stat exit"
                    break
        print "create_stat reulst:{0}".format(create_stat.to_string())
        print "acl_stat reulst:{0}".format(acl_stat.to_string())
        print "delete_stat reulst:{0}".format(delete_stat.to_string())


def main(argv):
    conf_file = './statbility_conf.json'
    if len(argv) > 1:
        conf_file = argv[1]

    fd = open(conf_file, 'r')
    conf_t = json.load(fd)
    fd.close()
    process_num = conf_t['process_num']
    process_list = []
    result_queue = Queue()
    counter = Counter(conf_t['max_count'])
    for i in range(0, process_num):
        p_t = JcacheAPIProcess(conf_t, result_queue, counter)
        p_t.start()
        process_list.append(p_t)

    stat_process = statProcess(result_queue, process_num)
    stat_process.start()

    for p in process_list:
        p.join()

    stat_process.join()


if __name__ == "__main__":
    main(sys.argv)
