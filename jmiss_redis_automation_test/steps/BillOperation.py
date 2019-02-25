#!/usr/bin/python
# coding:utf-8
import requests
import pytest
import logging
import json
info_logger = logging.getLogger(__name__)

def get_account_balance(url, token):
    header = {'token': token}
    account_balance = 0
    try:
        r = requests.get(url, headers = header, timeout = 20)
        account_balance = r.json()["data"]["accountBalance"]
    except:
        print "get_account_balance: Http request Error!"
    return account_balance


def compare_balance(before, after, bill):
    print "Before: " + str(before) + " After: " + str(after)
    print "consume: " + str(before - after) + " == " + str(bill)
    if before == after + bill:
        assert True
    elif 0 < before - after - bill < 9.99:
        assert True
    else:
        assert False



if __name__ == '__main__':
    get_account_balance('http://uc-inner-api-ite.jcloud.com/usercenter/getUser?pin=jcloudiaas2', 'stag')



