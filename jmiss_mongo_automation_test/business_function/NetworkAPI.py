# coding:utf-8

import logging

logger_info = logging.getLogger(__name__)

class Network(object):
    def __init__(self, conf_obj, data_obj, httpClient):
        self.conf_obj = conf_obj
        self.data_obj = data_obj
        self.httpClient = httpClient