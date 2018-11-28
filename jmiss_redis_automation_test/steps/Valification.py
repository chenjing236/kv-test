#!/usr/bin/python
# coding:utf-8
import logging
info_logger = logging.getLogger(__name__)



def checkNotFound(resp):
    if resp is None or resp.error is None:
        assert False
    assert int(resp.error.code) == 404

def assertInstance(resp, instance_id):
    if resp is not None and resp.result is not None:
        if resp.result["totalCount"] == 1:
            assert instance_id == resp.result["cacheInstances"][0]["cacheInstanceId"]
        else:
            assert False
    else:
        assert False

def assertRespNotNone(resp):
    assert resp is not None
    assert resp.error is None

##
##[{"configName":"hash-max-ziplist-entries","configValue":"256"}]
## vs
## {"hash-max-ziplist-entries":"256"}
##
def listCompareJason(list_data, json_data, policy):
    if len(list_data) == 0:
        assert False
    for item in list_data:
        assert item[policy["key"]] in json_data
        assert item[policy["value"]] == json_data[item[policy["key"]]]



def validateResult(result, data):
    if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
        print "type error"
        assert False
    for k, y in data.items():
        if k in result:
            if result[k] != y:
                print k,y,result[k]
                assert False
        else:
            assert False


def existResult(result, data):
    if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
        print "type error"
        assert False
    for k, y in data.items():
        if k not in result:
            print k, y
            assert False