#!/usr/bin/python
# coding:utf-8
from time import sleep

from jdcloud_sdk.services.redis.apis.CreateBackupRequest import *
from jdcloud_sdk.services.redis.apis.DescribeBackupPolicyRequest import DescribeBackupPolicyParameters, \
    DescribeBackupPolicyRequest
from jdcloud_sdk.services.redis.apis.DescribeBackupsRequest import DescribeBackupsParameters, DescribeBackupsRequest
from jdcloud_sdk.services.redis.apis.ModifyBackupPolicyRequest import ModifyBackupPolicyParameters, \
    ModifyBackupPolicyRequest
from jdcloud_sdk.services.redis.apis.RestoreInstanceRequest import RestoreInstanceParameters, RestoreInstanceRequest
from jdcloud_sdk.services.redis.apis.DescribeDownloadUrlRequest import DescribeDownloadUrlRequest,DescribeDownloadUrlParameters
from jmiss_redis_automation_test.steps.InstanceOperation import *


def create_backup(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = CreateBackupParameters(str(conf["region"]), instance_id, "intergrationTest", 1)
        request = CreateBackupRequest(params, header)

        resp = client_send(client, request)

        base_id=resp.result["baseId"]
        sleep(10)
        for i in range(0,1200):
            backups = query_backups(conf, instance_id, client, str(base_id))
            if backups!=None and backups.result["backups"][0]["backupStatus"]==2:
                break
            sleep(1)

    except Exception, e:
        print e

    return resp

def check_backup(conf,instance_id,base_id,client=None):
    if client is None:
        client = setClient(conf)

    resp_sdk=query_backups(conf,instance_id,client, base_id)
    backupSizeSdk=-1
    for backup in resp_sdk.result["backups"]:
        if backup["baseId"]==base_id:
            backupSizeSdk=int(resp_sdk.result["backups"][0]["backupSize"])
            break
    assert backupSizeSdk!=-1
    urlsSdk=get_download_url(conf,client,instance_id,base_id)

    resp_configmap = query_backups_configmap(conf, instance_id, "backup_" + base_id)
    resp_configmap = json.loads(resp_configmap)
    assert resp_configmap["is_success"]==True
    backupSizeConfigmap=0
    urlsConfigmap=[]

    findResult = re.findall("\"backupSizeByte\": (.*?)}", json.dumps(resp_configmap["ShardMap"]))
    for size in findResult:
        backupSizeConfigmap+=int(size)

    findResult = re.findall("\"backupUrl\": \"(.*?)\"", json.dumps(resp_configmap["ShardMap"]))
    for url in findResult:
        urlsConfigmap.append(url)

    assert backupSizeSdk==backupSizeConfigmap
    assert sorted(urlsSdk)==sorted(urlsConfigmap)
    return True


def get_download_url(conf,client,instance_id,base_id):
    global urls
    header = getHeader(conf)
    resp = None
    result=[]
    try:
        params = DescribeDownloadUrlParameters(conf["region"], instance_id, base_id)
        request = DescribeDownloadUrlRequest(params,header)

        resp = client_send(client, request)

        urls = resp.result["downloadUrls"]

    except Exception, e:
        print e
    for url in urls:
        result.append(str(url["link"].split('?',1)[0]))
    return result


def query_backups_configmap(conf, instance_id, base_id):
    data = {"key": base_id}
    _, _, resp = HttpClient.underlayEntry(conf, instance_id, "POST", "/getConfigmap", data)
    return resp["data"]


def query_backups(conf, instance_id, client=None, base_id=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeBackupsParameters(conf["region"], instance_id)
        params.setBaseId(base_id)
        request = DescribeBackupsRequest(params, header)

        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def query_backup_policy(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeBackupPolicyParameters(conf["region"], instance_id)
        request = DescribeBackupPolicyRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def reset_backup_policy(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = ModifyBackupPolicyParameters(conf["region"], instance_id, "18:30-18:30 +0800", "Monday")
        request = ModifyBackupPolicyRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp


def restore_instance(conf, instance_id, base_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = RestoreInstanceParameters(conf["region"], instance_id, base_id)
        request = RestoreInstanceRequest(params, header)
        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp