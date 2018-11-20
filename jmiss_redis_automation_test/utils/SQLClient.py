#!/usr/bin/python
# coding:utf-8
import MySQLdb
import time
import logging
info_logger = logging.getLogger(__name__)


class SQLClient(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def init_cursor(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor()

    def close_cursor(self):
        self.cursor.close()
        self.conn.close()

    def run(self, sql):
        self.init_cursor()
        return self.cursor.execute(sql)


    def exec_query_one(self, sql, allow_empty=False):
        n = self.run(sql)
        if n > 0:
            result_tuple = self.cursor.fetchone()
            self.close_cursor()
        elif allow_empty is True:
            result_tuple = (u'emptyResult',)
        else:
            self.close_cursor()
            info_logger.error("Failed to get results of sql:{0}".format(sql))
            assert False
        return result_tuple

    def exec_query_all(self, sql):
        n = self.run(sql)
        if n > 0:
            result_tuple = self.cursor.fetchall()
            self.close_cursor()
        else:
            self.close_cursor()
            info_logger.error("Failed to get results of sql:{0}".format(sql))
            assert False
        return result_tuple

    def wait_for_expectation(self, sql, expectation, wait_time=3, times=20, position=0, allow_empty=True):
        for i in range(0, times):
            result_tuple = self.exec_query_one(sql, allow_empty)
            if result_tuple[0] == "emptyResult":
                info_logger.info("NO data in DB!")
            elif expectation == result_tuple[position]:
                break
            info_logger.info("Query DB {0} times!".format(i + 1))
            time.sleep(wait_time)
        else:
            info_logger.error("Failed to get the expectation of {0}".format(expectation))
            assert False
        return result_tuple
