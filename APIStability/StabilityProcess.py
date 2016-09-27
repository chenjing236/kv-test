# coding=utf-8
from multiprocessing import Process, Lock
from Queue import Queue
import sys

from utils.JCacheUtils import *
from utils.WebClient import *
from utils.SQLClient import SQLClient
from utils.DockerClient import *
import random
import time
import os
import json


class Counter():
    def __init__(self, max_num, max_fail_num):
        self.locker = Lock()
        self.count = 0
        self.fail_count = 0
        self.max_num = max_num
        self.max_fail_num = max_fail_num

    def check(self, is_failed=False):
        res = True
        self.locker.acquire()
        self.count += 1
        # 暂时去掉最大数量限制，每跑10次输出一次结果
        # if self.max_num != 0 and self.count >= self.max_num:
        #     res = False
        if is_failed:
            self.fail_count += 1
        if self.max_fail_num != 0 and self.fail_count >= self.max_fail_num:
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
        dc = DockerClient(self.conf)
        wc = WebClient(self.conf['host'], self.conf['port'], self.conf['pin'], self.conf['auth_token'])
        sql_c = SQLClient(self.conf['mysql_host'], self.conf['mysql_port'], self.conf['mysql_user'], self.conf['mysql_passwd'],
                          self.conf['mysql_db'])
        idx = 1
        is_failed = False
        while True:
            if not self.counter.check(is_failed):
                self.res_queue.put(None)
                break
            pid = os.getpid()
            remarks = "remarks_{0}_{1}".format(pid, idx)
            name = "name_{0}_{1}".format(pid, idx)
            ca = CreateArgs(capacity=self.get_cap(), remarks=remarks, space_name=name)
            info_logger.info("\n--Start the {0} times run -----------------------------------------------------------"
                             "-----------".format(idx))
            # check create
            status, space_id = CreateCluster(wc, ca, sql_c)
            if status != 0:
                if space_id is not None:
                    DeleteCluster(wc, space_id, sql_c)
                self.res_queue.put((False, None, None, None, None, None))
                is_failed = True
                continue
            # check get cluster
            status, space_id, instances = CheckGetCluster(wc, space_id)
            get_cluster_check = True
            if status != 0:
                info_logger.error("check get cluster: the status of cluster error, status={0}".format(status))
                get_cluster_check = False
            if instances is None:
                info_logger.error("check get cluster: there is no instances in cluster:{0}".format(space_id))
                get_cluster_check = False



            # check redis memsize
            for instance in instances:
                check_redis_memsize = dc.inspect_container(instance['ip'], instance['port'])
            if instances is None:
                check_redis_memsize = False

            # check get clusters
            status, space_id = CheckGetClusters(wc, space_id)
            get_clusters_check = True
            if status != 0:
                get_clusters_check = False

            # check acl
            result = SetAcl(wc, space_id, sql_c, ["192.168.169.51", "192.168.169.87"])
            acl_check = True
            if result != 0:
                acl_check = False

            sleep_time = random.randint(0, self.max_sleep_time)
            time.sleep(sleep_time * 60)

            # check delete
            status = DeleteCluster(wc, space_id, sql_c)
            if status != 0:
                DeleteCluster(wc, space_id, sql_c)
                self.res_queue.put((True, get_cluster_check, check_redis_memsize, get_clusters_check, acl_check, False))
                is_failed = False
                continue
            self.res_queue.put((True, get_cluster_check, check_redis_memsize, get_clusters_check, acl_check, True))
            is_failed = False
            idx += 1


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
        get_cluster_stat = Stat()
        redis_memsize_stat = Stat()
        get_clusters_stat = Stat()
        acl_stat = Stat()
        delete_stat = Stat()
        exit_producer_num = 0
        idx = 0
        while True:
            if idx % 10 == 0 and idx > 0:  # 运行一段时间(指定个数)后输出一次结果
                stat_logger.info("create_stat result:{0}".format(create_stat.to_string()))
                stat_logger.info("get_cluster_stat result:{0}".format(get_cluster_stat.to_string()))
                stat_logger.info("redis_memsize_stat result:{0}".format(redis_memsize_stat.to_string()))
                stat_logger.info("get_clusters_stat result:{0}".format(get_cluster_stat.to_string()))
                stat_logger.info("acl_stat result:{0}".format(acl_stat.to_string()))
                stat_logger.info("delete_stat result:{0}\n".format(delete_stat.to_string()))
            res = self.result_queue.get()
            if res is not None:
                create_res, get_cluster_res, redis_memsize_res, get_clusters_res, acl_res, delete_res = res
                if create_res is not None:
                    create_stat.add(create_res)
                if get_cluster_res is not None:
                    get_cluster_stat.add(get_cluster_res)
                if redis_memsize_res is not None:
                    redis_memsize_stat.add(redis_memsize_res)
                if get_clusters_res is not None:
                    get_clusters_stat.add(get_clusters_res)
                if acl_res is not None:
                    acl_stat.add(acl_res)
                if delete_res is not None:
                    delete_stat.add(delete_res)
                idx += 1
            else:
                exit_producer_num += 1
                if exit_producer_num >= self.producer_num:
                    print "process stat exit"
                    break
        stat_logger.info("create_stat result:{0}".format(create_stat.to_string()))
        stat_logger.info("get_cluster_stat result:{0}".format(get_cluster_stat.to_string()))
        stat_logger.info("redis_memsize_stat result:{0}".format(redis_memsize_stat.to_string()))
        stat_logger.info("get_clusters_stat result:{0}".format(get_cluster_stat.to_string()))
        stat_logger.info("acl_stat result:{0}".format(acl_stat.to_string()))
        stat_logger.info("delete_stat result:{0}\n".format(delete_stat.to_string()))


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
    counter = Counter(conf_t['max_num'], conf_t['max_fail_num'])
    for i in range(0, process_num):
        p_t = JcacheAPIProcess(conf_t, result_queue, counter)
        p_t.run()
        process_list.append(p_t)

    stat_process = statProcess(result_queue, process_num)
    stat_process.run()

    for p in process_list:
        p.join()

    stat_process.join()


if __name__ == "__main__":
    main(sys.argv)
