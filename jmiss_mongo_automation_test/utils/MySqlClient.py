#!/usr/bin/python
# coding:utf-8
import MySQLdb
import json
class MysqlClient(object):
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

    def get_instances(self, space_id):
        '''
        :param space_id:
        :return: [primary, secondary, hidden]
        '''
        self.init_cursor()
        sql = "select docker_id, host_ip, domain, instance_ip from instance where space_id='{0}'".format(space_id)
        n = self.cursor.execute(sql)
        if n < 2:
            return None
        if n < 3:
	    raise Exception("get instance num:{0} != 3".format(n))
            return list(self.cursor.fetchall())
        ins = list(self.cursor.fetchall())
        self.close_cursor()
        return ins
    def get_backup_info(self,operation_id):
        self.init_cursor()
        sql = "select name,status from backup where request_id = '{0}'".format(operation_id)
        n = self.cursor.execute(sql)
        if n<1:
            return None
        ins = list(self.cursor.fetchall())
        self.close_cursor()
        return ins