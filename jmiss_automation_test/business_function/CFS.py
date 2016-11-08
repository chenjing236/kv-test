#!/usr/bin/python
# coding:utf-8
import hashlib
import httplib
import json
from datetime import datetime

class CFS:
    def __init__(self, conf_obj):
        self.cfs_host = conf_obj["cfs_host"]
        self.sign_key = conf_obj["cfs_sign_key"]

    def http_request(self, method, uri, data=None, headers={}):
        hc = httplib.HTTPConnection(self.cfs_host)
        hc.request(method, uri, data, headers)
        res = hc.getresponse()
        status = res.status
        data = res.read()
        #print data
        res_data = json.loads(data)
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def get_timestr(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def md5sign(self, space_id, t):
        source_str = self.sign_key + space_id + t
        m = hashlib.md5()
        m.update(source_str)
        #print source_str
        return m.hexdigest()

    def get_meta(self, space_id):
        cur_time = self.get_timestr()
        time_str = cur_time.replace(":", "%3A").replace(" ", "+")
        uri = "/manage/topology/get?spaceId={0}&d={1}&s={2}".format(space_id, time_str, self.md5sign(space_id, cur_time))
        status, headers, res_data = self.http_request("GET", uri)
        if status != 200 or res_data['code'] != 0:
            return None
        return res_data['data']

    def get_topology_from_cfs(self, tp):
        if 'shards' not in tp or tp['shards'] is None or len(tp['shards']) == 0 or 'master' not in tp['shards'][0]:
            return None, None, None, None
        else:
            master = tp['shards'][0]['master']
            master_ip = master['ip']
            master_port = master['port']
        if 'slaves' not in master or master['slaves'] is None or len(master['slaves']) == 0:
            slaveIp = None
            slavePort = None
        else:
            slave = master['slaves'][0]
            slaveIp = slave['ip']
            slavePort = slave['port']
        return master_ip, master_port, slaveIp, slavePort

if __name__ == "__main__":
    config_file_path = "C:/Users/guoli5/git/JCacheTest/jmiss_automation_test/config/conf.json"
    config = json.load(open(config_file_path, 'r'))
    cfs_client = CFS(config)
    space_id = "d1e07a0f-7dc0-46d0-94f8-34ea471e2092"
    res_data = cfs_client.get_meta("d1e07a0f-7dc0-46d0-94f8-34ea471e2092")
    print "[INFO] Topology of CFS is {0}".format(res_data)
    epoch = res_data["epoch"]
    print "[INFO] Epoch is {0} before failover".format(epoch)
    currentTopology = res_data["currentTopology"]
    master_ip, master_port, slaveIp, slavePort = cfs_client.get_topology_from_cfs(currentTopology)
    print "[INFO] Topology of the instance {0} is {1}:{2}, {3}:{4}".format(space_id,master_ip, master_port, slaveIp, slavePort)