import MySQLdb
import json
from JCacheUtils import *

class SQLClient(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
    def init_cursor(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor()

    def close_cursor(self):
        self.cursor.close()
        self.conn.close()
    def run(self, sql):
        return self.cursor.execute(sql)

    def get_space_status(self, space_id):
        '''
        :param space_id: space if
        :return: (status,capacity,password,flag,tenant_id,remarks)
        '''
        info_logger.debug("begin to get space info, space_id[{0}]".format(space_id))
        self.init_cursor()
        sql = "select status,capacity,password,cluster_type,tenant_id,name,remarks from space where space_id='{0}'".format(space_id)
        n = self.cursor.execute(sql)
        if n < 1:
            return None
        if n != 1:
            raise Exception("get more than one record in space table, space_id:{0}".format(space_id))
        res = self.cursor.fetchall()[0]
        self.close_cursor()
        info_logger.debug("get space info success![{0}]".format(json.dumps(res)))
        return res

    def get_instances(self, space_id):
        '''
        :param space_id:
        :return: [master,slave(ip,port,copy_id,flag)]
        '''
        info_logger.debug("begin to get instances, space_id:[{0}]".format(space_id))
        self.init_cursor()
        sql = "select ip,port,copy_id,shard_id from instance where space_id='{0}'".format(space_id)
        n = self.cursor.execute(sql)
        if n < 1:
            return None
        if n < 2:
            raise Exception("get instance num:{0} != 2".format(n))
        ins = list(self.cursor.fetchall())
        if ins[0][2] != 'm':
            tmp = ins[0]
            ins[0] = ins[1]
            ins[1] = tmp
        self.close_cursor()
        info_logger.debug("get instances success:{0}".format(json.dumps(ins)))
        return ins

    def get_acl(self, space_id):
        self.init_cursor()
        sql = "select src_ip,tenant_id from acl where space_id='{0}'".format(space_id)
        self.cursor.execute(sql)
        ips = self.cursor.fetchall()
        acl_ip = []
        t_id = None
        for ip, tenant in ips:
            if t_id is not None:
                if t_id != tenant:
                    raise Exception("tenant_id of one cluster is different in acl table![{0},{1}]".format(t_id, tenant))
            t_id = tenant
            if ip not in acl_ip:
                acl_ip.append(ip)
        self.close_cursor()
        return acl_ip

    def get_domain(self, space_id):
        self.init_cursor()
        sql = "select domain from ap where space_id='{0}'".format(space_id)
        n = self.cursor.execute(sql)
        if n > 1:
            raise Exception("get > 1 record")
        if n < 1:
            return None
        res = self.cursor.fetchall()[0][0]
        self.close_cursor()
        return res

    def get_token(self, space_id):
        self.init_cursor()
        sql = "select password from space where space_id='{0}'".format(space_id)
