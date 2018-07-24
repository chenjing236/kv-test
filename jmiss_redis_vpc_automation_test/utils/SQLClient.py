#!/usr/bin/python
# coding:utf-8
from conftest import *
import MySQLdb
# import json
import time
import logging
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


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

    def get_ap_ip(self, space_id):
        sql_ap = "select docker_id,overlay_ip from ap where space_id='{0}'".format(space_id)
        n = self.run(sql_ap)
        docker_id = 0
        ap_ip = 0
        if n > 0:
            ap_list = self.cursor.fetchall()
            docker_id = ap_list[0][0]
            ap_ip = ap_list[0][1]
        self.close_cursor()
        return docker_id, ap_ip, ap_list

    def check_scaler_task(self, space_id, expectation, times):
        sql_scaler_task = "select id,return_code FROM `scaler_task` WHERE space_id='{0}' order by id desc".format(
            space_id)
        task_id = 0
        return_code = 2
        for i in range(0, times):
            n = self.run(sql_scaler_task)
            if n > 0:
                info = self.cursor.fetchone()
                task_id = info[0]
                return_code = info[1]
            if expectation == return_code:
                info_logger.info("[DB_INFO] Check return code is {0}".format(return_code))
                break
            info_logger.info("[DB_INFO] Check return code is {0}".format(return_code))
            time.sleep(3)
        else:
            info_logger.info("[ERROR] Failed to get the expectation of {0}".format(expectation))
            assert False
        self.close_cursor()

        return task_id, return_code

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
