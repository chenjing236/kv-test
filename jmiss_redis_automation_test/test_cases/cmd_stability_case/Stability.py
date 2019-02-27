# coding=utf-8
from concurrent.futures import ThreadPoolExecutor, wait
import random
from commands import *
import re
import json
import sys


# 截取线程地址，用于唯一标识线程
def find_add(f):
    regex = "0x[0-9a-f]{12}"
    return re.search(regex, str(f)).group()


class Stability:
    def __init__(self, config):
        self.config = config

    # 执行case
    def run_command(self, case, db, sec):
        print "cases execute times: ", case_num
        case_num[case] += 1
        time.sleep(2)
        globals()[case](host=self.config['host'], port=self.config['port'], db=db, password=self.config['password'], sec=sec)

    def stability_test(self):
        # 最大并发数，线程池大小
        executor = ThreadPoolExecutor(max_workers=self.config['thread_num'])
        # 执行命令的db_num，256个db轮询执行
        db_num = self.config['dbnum_start']
        # 记录线程与db num对应关系的map(pid, db_num)
        f_list = {}

        for i in range(self.config['thread_num']):
            random_case = random.sample(cases, 1)[0]
            run_time = random.randint(self.config['runtime_start'], self.config['runtime_end'])
            future = executor.submit(self.run_command, random_case, db_num, run_time)
            db_num = (db_num + 1) % 256
            f_list[find_add(future)] = db_num
        while True:
            hello = wait(f_list, return_when='FIRST_COMPLETED', timeout=2)
            # hello[0]为已完成线程列表, 在f_list中删除已完成线程
            for j in hello[0]:
                del f_list[find_add(j)]
            # hello[1]为未完成线程列表
            if len(hello[1]) >= self.config['thread_num']:
                continue
            random_case = random.sample(cases, 1)[0]
            run_time = random.randint(self.config['runtime_start'], self.config['runtime_end'])
            future = executor.submit(self.run_command, random_case, db_num, run_time)
            # db_num到达255后，重新从0开始循环
            db_num = (db_num + 1) % 256
            # 当前被线程占用的db_num
            db_arr = f_list.values()
            # 如果有未执行完的线程占用某db，则跳过这个db
            while db_num in db_arr:
                db_num = (db_num + 1) % 256
            f_list[find_add(future)] = db_num


def main():
    conf_file = sys.argv[1]
    # conf_file = './config/config_hb_cluster.json'
    fd = open(conf_file, 'r')
    conf = json.load(fd)
    fd.close()
    stability = Stability(conf)
    stability.stability_test()

if __name__ == "__main__":
    main()
