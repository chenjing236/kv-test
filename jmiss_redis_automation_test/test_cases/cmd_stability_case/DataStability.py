# coding=utf-8

import json
import sys
import redis
import time


class DataStability:
    def __init__(self, config):
        self.config = config
        self.exec_times = self.config["exec_times"]
        self.db_num = self.config['dbnum']
        self.err_num = 0

    def set_get_keys(self):
        r = redis.Redis(host=self.config["host"], port=self.config["port"], db=self.db_num, password=self.config["password"])
        for i in range(self.exec_times):
            # set
            set_result = r.set('stab_set_key', 'stab_set_value')
            if set_result is not True:
                self.err_num += 1
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "【ERROR】Set key error! set key return [{0}]".format(set_result)
            # get
            get_result = r.get('stab_set_key')
            if get_result != 'stab_set_value':
                self.err_num += 1
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "【ERROR】Get key error! get key return [{0}]".format(get_result)
            # time.sleep(0.01)
        return self.err_num * 100.0 / 2.0 / self.exec_times


def main():
    if len(sys.argv) == 2:
        conf_file = sys.argv[1]
    # 参数数量错误
    else:
        print "Arguments Error! It should be \"python DataStability.py config_file\""
        return
    # conf_file = './config/config_hb_cluster.json'
    fd = open(conf_file, 'r')
    conf = json.load(fd)
    fd.close()
    stability = DataStability(conf)
    # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    err_rate = stability.set_get_keys()
    # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print "err_num is {0}".format(stability.err_num)
    # print "err_rate is {0}%".format(err_rate)
    print "tags:region:{0}".format(stability.config["region"])
    print "cmd_err_rate:{0}".format(err_rate)

if __name__ == "__main__":
    main()
