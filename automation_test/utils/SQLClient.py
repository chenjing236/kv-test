#!/usr/bin/python
#coding:utf-8
import MySQLdb

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
        self.init_cursor()
        return self.cursor.execute(sql)

    def get_space_status(self, space_id):
        '''
        :param space_id: space if
        :return: (status,capacity,password,flag,tenant_id,remarks)
        '''
        print "begin to get space info, space_id[{0}]".format(space_id)
        self.init_cursor()
        sql = "select status,capacity,password,flag,tenant_id,name,remarks from space where id={0}".format(space_id)
        n = self.cursor.execute(sql)
        if n < 1:
            return None
        if n != 1:
            raise Exception("get more than one record in space table, space_id:{0}".format(space_id))
        res = self.cursor.fetchall()[0]
        self.close_cursor()
        print "get space info success![{0}]".format(res)
        return res

    def get_instances(self, space_id):
        '''
        :param space_id:
        :return: [master,slave(ip,port,copy_id,flag)]
        '''
        print "begin to get instances, space_id:[{0}]".format(space_id)
        self.init_cursor()
        sql = "select ip,port,copy_id,flag from instance where space_id={0}".format(space_id)
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
        print "get instances success: [{0}]".format(ins)
        return ins

    def get_acl(self, space_id):
        self.init_cursor()
        sql = "select src_ip,tenant_id from acl where space_id={0}".format(space_id)
        self.cursor.execute(sql)
        ips = self.cursor.fetchall()
        acl_ip = []
        t_id = None
        for ip,tenant in ips:
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
        sql = "select domain from ap where space_id={0}".format(space_id)
        n = self.cursor.execute(sql)
        if n > 1:
            raise Exception("get > 1 record")
        if n < 1:
            return None
        res = self.cursor.fetchall()[0][0]
        self.close_cursor()
        return res

    #根据space id查看instance表中slave的IP和Port
    def get_slave_ip_port(self,space_id):
        '''
        :param space_id:
        :return: [slave(ip,port)]
        '''
        self.sql_slave = "select ip,port from instance where space_id={0} and copy_id!='m'".format(space_id)
        n = self.run(self.sql_slave)
        slave_ip = 0
        slave_port = 0
        if n > 0:
            slave_info = list(self.cursor.fetchall())
            slave_ip = slave_info[0][0]
            slave_port = slave_info[0][1]
        self.close_cursor()

        return slave_ip,slave_port

    #根据space_id查看instance表中master的IP和Port
    def get_master_ip_port(self,space_id):
        '''
        :param space_id:
        :return: [master(ip,port)]
        '''
        self.sql_master = "select ip,port from instance where space_id={0} and copy_id='m'".format(space_id)
        n = self.run(self.sql_master)
        master_ip = 0
        master_port = 0
        if n > 0:
            master_info = list(self.cursor.fetchall())
            master_ip = master_info[0][0]
            master_port = master_info[0][1]
        self.close_cursor()

        return master_ip,master_port

sql_client = SQLClient("192.168.177.87", 3306, "jimdb", "jimdbtest", "jimdb")

res = sql_client.get_space_status(146)
print res
res = sql_client.get_instances(104)
print res
res = sql_client.get_acl(1041)
print res
res = sql_client.get_domain(1041)
print res
