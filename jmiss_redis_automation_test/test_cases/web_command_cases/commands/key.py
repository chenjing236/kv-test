#!/usr/bin/python
# coding:utf-8
from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command


def del_command(config, instance_id, region, *key):
    cmd = "del " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def dump_command(config, instance_id, region, *key):
    cmd = "dump " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def exists_command(config, instance_id, region, *key):
    cmd = "exists " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def expire_command(config, instance_id, region, *key):
    cmd = "del " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def expireat_command(config, instance_id, region, *key):
    cmd = "expireat " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def keys_command(config, instance_id, region, *key):
    cmd = "keys " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def persist_command(config, instance_id, region, *key):
    cmd = "persist " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def pexpire_command(config, instance_id, region, *key):
    cmd = "pexpire " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def pexpireat_command(config, instance_id, region, *key):
    cmd = "pexpireat " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def pttl_command(config, instance_id, region, *key):
    cmd = "pttl " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def restore_command(config, instance_id, region, *key):
    cmd = "restore " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def sort_command(config, instance_id, region, *key):
    cmd = "sort " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def ttl_command(config, instance_id, region, *key):
    cmd = "ttl " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def type_command(config, instance_id, region, *key):
    cmd = "type " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp


def scan_command(config, instance_id, region, *key):
    cmd = "scan " + tuple_to_str(key)
    resp = send_web_command(config, instance_id, region, cmd)
    return resp
