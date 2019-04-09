# coding=utf-8
from concurrent.futures import ThreadPoolExecutor, wait
import random
from commands import *
import re
import json
import sys


# 截取线程地址，用于唯一标识线程
def find_add(f):
    add = ''
    try:
        regex = "0x[0-9a-f]+\s+"
        add = re.search(regex, str(f)).group()[0:-1]
    except Exception, err:
        print "【ERROR】run find_add error [{0}], pid is {1}".format(err, f)
    return add


class Stability:
    def __init__(self, config, exec_times=-1):
        self.config = config
        self.exec_times = int(exec_times)
        self.executor = ThreadPoolExecutor(max_workers=config['thread_num'])  # 最大并发数，线程池大小
        self.db_num = self.config['dbnum_start']  # 执行命令的db_num，256个db轮询执行
        self.f_list = {}  # 记录线程列表及db_num的对应关系
        self.p_list = []  # 记录线程列表

    # 执行case
    def run_command(self, db):
        case = random.sample(cases, 1)[0]
        run_time = random.randint(self.config['runtime_start'], self.config['runtime_end'])
        print "cases execute times: ", case_num
        case_num[case] += 1
        time.sleep(2)
        globals()[case](host=self.config['host'], port=self.config['port'], db=db, password=self.config['password'], sec=run_time)

    # new thread
    def start_new_task(self):
        # 当前被线程占用的db_num
        db_arr = self.f_list.values()
        # 如果有未执行完的线程占用此db，则跳过这个db
        while self.db_num in db_arr:
            self.db_num = (self.db_num + 1) % 256
        future = self.executor.submit(self.run_command, self.db_num)
        add = find_add(future)
        # 获取地址失败，返回失败
        if add == '':
            return False
        # 新建的任务插入记录列表
        self.p_list.append(future)
        self.f_list[add] = self.db_num
        self.exec_times -= 1
        # db_num ++
        self.db_num = (self.db_num + 1) % 256
        return True

    def stability_test(self):
        while True:
            hello = wait(self.p_list, return_when='ALL_COMPLETED', timeout=3)
            # hello[0]为已完成任务列表, 在f_list中删除已完成任务
            # hello[1]为未完成任务列表
            for j in hello[0]:
                self.p_list.remove(j)
                del self.f_list[find_add(j)]

            # 限制任务数不超过线程池大小
            if len(hello[1]) >= self.config['thread_num']:
                continue
            else:
                # case执行完成，没有剩余任务，结束执行
                if self.exec_times == 0 and len(hello[1]) == 0:
                    print "【FINISHED】cases execute times: ", case_num
                    break
                # case执行完成，等待剩余任务执行完成
                elif self.exec_times == 0 and len(hello[1]) != 0:
                    continue
                # else self.exec_times > 0, 还未达到次数限制，继续执行
                # else: self.exec_times < 0, 没有次数限制，新建case执行

            # 插入新的任务
            self.start_new_task()


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
