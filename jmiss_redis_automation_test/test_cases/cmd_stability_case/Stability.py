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
    def __init__(self, config, exec_times=-1):
        self.config = config
        self.exec_times = int(exec_times)

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
        # 记录线程列表
        p_list = []

        for i in range(self.config['thread_num']):
            random_case = random.sample(cases, 1)[0]
            run_time = random.randint(self.config['runtime_start'], self.config['runtime_end'])
            future = executor.submit(self.run_command, random_case, db_num, run_time)
            db_num = (db_num + 1) % 256
            p_list.append(future)
            f_list[find_add(future)] = db_num
            self.exec_times -= 1
        while True:
            hello = wait(p_list, return_when='FIRST_COMPLETED', timeout=2)
            # hello[0]为已完成任务列表, 在f_list中删除已完成任务
            # hello[1]为未完成任务列表
            for j in hello[0]:
                p_list.remove(j)
                del f_list[find_add(j)]

            # 限制任务数不超过线程池大小
            if len(hello[1]) >= self.config['thread_num']:
                continue
            else:
                # 新建case执行，执行计数-1
                if self.exec_times > 0:
                    self.exec_times -= 1
                # case执行完成，没有剩余任务，结束执行
                elif self.exec_times == 0 and len(hello[1]) == 0:
                    print "cases execute times: ", case_num
                    break
                # case执行完成，等待剩余任务执行完成
                elif self.exec_times == 0 and len(hello[1]) != 0:
                    continue
                # else: self.exec_times < 0, 没有次数限制，新建case执行
            # 生成随机执行case
            random_case = random.sample(cases, 1)[0]
            # 生成随机执行时长
            run_time = random.randint(self.config['runtime_start'], self.config['runtime_end'])
            future = executor.submit(self.run_command, random_case, db_num, run_time)
            # db_num到达255后，重新从0开始循环
            db_num = (db_num + 1) % 256
            # 当前被线程占用的db_num
            db_arr = f_list.values()
            # 如果有未执行完的线程占用某db，则跳过这个db
            while db_num in db_arr:
                db_num = (db_num + 1) % 256
            p_list.append(future)
            f_list[find_add(future)] = db_num


def main():
    exec_times = -1
    # 不设置执行次数，case无限循环
    if len(sys.argv) == 2:
        conf_file = sys.argv[1]
        print "Not set exec_times, stability cases always run!"
    # 设置执行次数exec_times
    elif len(sys.argv) == 3 and int(sys.argv[2]) > 0:
        conf_file = sys.argv[1]
        exec_times = sys.argv[2]
        print "Stability cases exec {0} times".format(exec_times)
    # 参数错误
    else:
        print "Arguments Error! It should be \"python Stability.py config_file [exec_times(>0)]\""
        return
    # conf_file = './config/config_hb_cluster.json'
    fd = open(conf_file, 'r')
    conf = json.load(fd)
    fd.close()
    stability = Stability(conf, exec_times)
    stability.stability_test()

if __name__ == "__main__":
    main()
