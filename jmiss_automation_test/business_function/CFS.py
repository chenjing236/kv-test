# coding:utf-8
import hashlib
import httplib
import json
from datetime import datetime
import logging

logger_info = logging.getLogger(__name__)

class CFS:
    def __init__(self, host, conf_obj, capacity='16777216'):
        self.cfs_host = host
        self.sign_key = conf_obj["cfs_sign_key"]
        self.shard_count = conf_obj["cluster_cfg"][str(int(capacity) / 1024 / 1024)]

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
        logger_info.debug("[INFO] URI for cfs is %s", uri)
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

    def get_topology_of_cluster_from_cfs(self, tp):
        shards = []
        for i in range(0, self.shard_count):
            if 'shards' not in tp or tp['shards'] is None or len(tp['shards']) == 0 or 'master' not in tp['shards'][i]:
                return None
            else:
                master = tp['shards'][i]['master']
                master_ip = master['ip']
                master_port = master['port']
            if 'slaves' not in master or master['slaves'] is None or len(master['slaves']) == 0:
                slave_ip = None
                slave_port = None
            else:
                slave = master['slaves'][0]
                slave_ip = slave['ip']
                slave_port = slave['port']
            shard = {"masterIp": master_ip, "masterPort": master_port, "slaveIp": slave_ip, "slavePort": slave_port}
            shards.append(shard)
        return shards
