#!/usr/bin/python
# coding:utf-8
from jdcloud_sdk.services.redis.apis.CreateBackupRequest import *
from jdcloud_sdk.services.redis.apis.DescribeBackupPolicyRequest import DescribeBackupPolicyParameters, \
    DescribeBackupPolicyRequest
from jdcloud_sdk.services.redis.apis.DescribeBackupsRequest import DescribeBackupsParameters, DescribeBackupsRequest
from jdcloud_sdk.services.redis.apis.ModifyBackupPolicyRequest import ModifyBackupPolicyParameters, \
    ModifyBackupPolicyRequest
from jdcloud_sdk.services.redis.apis.RestoreInstanceRequest import RestoreInstanceParameters, RestoreInstanceRequest

from jmiss_redis_automation_test.steps.InstanceOperation import *


def create_backup(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = CreateBackupParameters(str(conf["region"]), instance_id, conf["backup"]["name"], 1)
        request = CreateBackupRequest(params, header)

        resp = client_send(client, request)
    except Exception, e:
        print e

    return resp



def query_backups(conf, instance_id, client=None):
    if client is None:
        client = setClient(conf)
    header = getHeader(conf)
    resp = None
    try:
        params = DescribeBackupsParameters(conf["region"], instance_id)
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