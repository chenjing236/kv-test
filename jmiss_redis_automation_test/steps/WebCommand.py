#!/usr/bin/python
# coding:utf-8
from collections import OrderedDict
from time import sleep

from jmiss_redis_automation_test.steps.FusionOpertation import send_web_command, proc_web_command_result, \
    find_resp_error
from jmiss_redis_automation_test.steps.InstanceOperation import setClient
from jmiss_redis_automation_test.steps.Valification import assertRespNotNone


class WebCommand():
    def __init__(self, conf, instance_id, region, token):
        self.conf = conf
        self.instance_id = instance_id
        self.region = region
        self.token = token
        self.client = setClient(conf)

    def set_command_exceptedResp(self, command, excepted_resp):
        self.command = command
        self.excepted_resp = excepted_resp

    def runCommandAndCheckResp(self):
        resp = send_web_command(self.conf, self.instance_id, self.region, self.command, self.client, self.token)
        assertRespNotNone(resp)
        if self.excepted_resp == None:
            return find_resp_error(resp.result["commandResult"])
        result = proc_web_command_result(resp.result["commandResult"])
        return sorted(result) == sorted(self.excepted_resp)

    def runCommand(self):
        resp = send_web_command(self.conf, self.instance_id, self.region, self.command, self.client, self.token)
        assertRespNotNone(resp)
        return True

    def runAllCommand(self):
        for (cmd, excepted_resp) in typeKeyCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeStringCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeHashCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeListCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeSetCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeZsetCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeConnectionCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeServerCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeScriptingCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeHyperLogLogCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

        for (cmd, excepted_resp) in typeGeoCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommand()
            sleep(0.1)

    def runAllForeverCommand(self):
        while True:
            for (cmd, excepted_resp) in typeKeyCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeStringCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeHashCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeListCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeSetCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeZsetCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeConnectionCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeServerCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeScriptingCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeHyperLogLogCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

            for (cmd, excepted_resp) in typeGeoCommand.items():
                self.set_command_exceptedResp(cmd, excepted_resp)
                assert self.runCommand()
                sleep(0.1)

    def checkAllCommandAndResp(self):
        for (cmd, excepted_resp) in typeKeyCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeStringCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeHashCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeListCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeSetCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeZsetCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeConnectionCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeServerCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeScriptingCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeHyperLogLogCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)

        for (cmd, excepted_resp) in typeGeoCommand.items():
            self.set_command_exceptedResp(cmd, excepted_resp)
            assert self.runCommandAndCheckResp()
            sleep(0.1)


typeKeyCommand = OrderedDict([("SET test_key test_key", ["OK"]),
                              # "DUMP test_key", "\x00\xc0{\a\x00\xb7\xd0\x86\x12\b\xb0\xb2\xa3",
                              ("EXISTS test_key", ["1"]),
                              ("EXPIRE test_key 1000", ["1"]),
                              ("EXPIREAT test_key 2524579200", ["1"]),
                              # "KEYS*", "",
                              ("PERSIST test_key", ["1"]),
                              ("PEXPIRE test_key 1000000", ["1"]),
                              ("PEXPIREAT test_key 2524579200000", ["1"]),
                              ("PTTL test_key", None),
                              # "RESTORE test_key 0 \x00\xc0{\a\x00\xb7\xd0\x86\x12\b\xb0\xb2\xa3", "OK",
                              ("LPUSH today_cost 30 1.5 10 8", ["4"]),
                              ("SORT today_cost", ["1.5", "8", "10", "30"]),
                              ("TTL test_key", None),
                              ("TYPE test_key", ["string"]),
                              ("DEL test_key", ["1"]),
                              ("SCAN 0", None),
                              ("SET test_key1 test_key1", ["OK"]),
                              ("OBJECT REFCOUNT test_key1", ["1"]),
                              ("OBJECT IDLETIME test_key1", None),
                              ("OBJECT ENCODING test_key1", ["embstr"]),
                              ("TOUCH test_key1", ["1"]),
                              ("UNLINK test_key1", ["1"]),
                              ("BITOP NOT test_key1 test_key1", ["0"]),
                              ("MOVE test_key1 1", ["0"])
                              ])

typeStringCommand = OrderedDict([("APPEND test_string_key 100", ["3"]),
                                 ("BITCOUNT test_string_key", ["7"]),
                                 ("BITPOS test_string_key 1", ["2"]),
                                 ("DECR test_string_key", ["99"]),
                                 ("DECRBY test_string_key 1", ["98"]),
                                 ("GET test_string_key", ["98"]),
                                 ("GETBIT test_string_key 1", ["0"]),
                                 ("GETRANGE test_string_key 0 4", ["98"]),
                                 ("GETSET test_string_key 100", ["98"]),
                                 ("INCR test_string_key", ["101"]),
                                 ("INCRBY test_string_key 10", ["111"]),
                                 ("INCRBYFLOAT test_string_key 2.5", ["113.5"]),
                                 ("MGET test_string_key", ["113.5"]),
                                 ("MSET test_string_key test_string_key", ["OK"]),
                                 ("PSETEX test_string_key 10000000 100", ["OK"]),
                                 ("SET test_string_key 100", ["OK"]),
                                 ("SETBIT test_string_key 5 1", ["0"]),
                                 ("SETEX test_string_key 1000 100", ["OK"]),
                                 ("SETNX test_string_key 100", ["0"]),
                                 ("SETRANGE test_string_key 3 123456", ["9"]),
                                 ("STRLEN test_string_key", ["9"])
                                 ])

typeHashCommand = OrderedDict([("HMSET test_hash_key hlc 100", ["OK"]),
                               ("HEXISTS test_hash_key hlc", ["1"]),
                               ("HGET test_hash_key hlc", ["100"]),
                               ("HGETALL test_hash_key", ["hlc", "100"]),
                               ("HINCRBY test_hash_key hlc 100", ["200"]),
                               ("HINCRBYFLOAT test_hash_key hlc 50.9", ["250.89999999999999999"]),
                               ("HKEYS test_hash_key", ["hlc"]),
                               ("HLEN test_hash_key", ["1"]),
                               ("HMGET test_hash_key hlc", ["250.89999999999999999"]),
                               ("HSET test_hash_key redis redis", ["1"]),
                               ("HSETNX test_hash_key test1 test1", ["1"]),
                               ("HVALS test_hash_key", ["250.89999999999999999", "redis", "test1"]),
                               ("HSCAN test_hash_key 0", None),
                               ("HSTRLEN test_hash_key hlc", ["21"]),
                               ("HDEL test_hash_key hlc", ["1"])
                               ])

typeListCommand = OrderedDict([("LPUSH test_list_key hlc hlc1 hlc2", ["3"]),
                               ("LINDEX test_list_key 0", ["hlc2"]),
                               ("LINSERT test_list_key BEFORE hlc test10", ["4"]),
                               ("LLEN test_list_key", ["4"]),
                               ("LPOP test_list_key", ["hlc2"]),
                               ("LPUSHX test_list_key hlc1", ["4"]),
                               ("LRANGE test_list_key 0 -1", ["hlc1", "hlc1", "test10", "hlc"]),
                               ("LREM test_list_key 1 test1", ["0"]),
                               ("LSET test_list_key 0 test2", ["OK"]),
                               ("LTRIM test_list_key 1 -1", ["OK"]),
                               ("RPOP test_list_key", ["hlc"]),
                               ("RPUSH test_list_key test3", ["3"]),
                               ("RPUSHX test_list_key test4", ["4"]),
                               # ("BLPOP test_list_key 180", None),
                               # ("BRPOP test_list_key 180", None),
                               # ("BRPOPLPUSH test_list_key test_list_key1 180", None),
                               # ("BLPOP test_list_key2 180", None),
                               ])

typeSetCommand = OrderedDict([("SADD test_set_key hlc1 hlc2 hlc3", ["3"]),
                              ("SCARD test_set_key", ["3"]),
                              ("SISMEMBER test_set_key hlc1", ["1"]),
                              ("SMEMBERS test_set_key ", ["hlc2", "hlc1", "hlc3"]),
                              ("SREM test_set_key hlc1", ["1"]),
                              ("SPOP test_set_key", None),
                              ("SRANDMEMBER test_set_key", None),
                              ("SSCAN test_set_key 0", None)
                              ])

typeZsetCommand = OrderedDict([("ZADD test_zset_key 1 hlc1 2 hlc2 3 hlc3 4 hlc4 5 hlc5 6 hlc6", ["6"]),
                               ("ZCARD test_zset_key", ["6"]),
                               ("ZCOUNT test_zset_key 0 10", ["6"]),
                               ("ZINCRBY test_zset_key 10 hlc1", ["11"]),
                               ("ZRANGE test_zset_key 0 1", ["hlc2", "hlc3"]),
                               ("ZRANGEBYSCORE test_zset_key 0 5", ["hlc2", "hlc3", "hlc4", "hlc5"]),
                               ("ZRANK test_zset_key hlc1", ["5"]),
                               ("ZREM test_zset_key hlc3", ["1"]),
                               ("ZREMRANGEBYRANK test_zset_key -2 -1", ["2"]),
                               ("ZREMRANGEBYSCORE test_zset_key -2 -1", ["0"]),
                               ("ZREVRANGE test_zset_key 0 1", ["hlc5", "hlc4"]),
                               ("ZREVRANGEBYSCORE test_zset_key 10 0", ["hlc5", "hlc4", "hlc2"]),
                               ("ZREVRANK test_zset_key hlc4", ["1"]),
                               ("ZSCORE test_zset_key hlc4", ["4"]),
                               ("ZSCAN test_zset_key 0", None),
                               ("ZADD myzset 0 aaaa 0 b 0 c 0 d 0 e", ["5"]),
                               ("ZRANGEBYLEX myzset [alpha [omega", ["b", "c", "d", "e"]),
                               ("ZLEXCOUNT myzset - +", ["5"]),
                               ("ZREMRANGEBYLEX myzset [alpha [omega", ["4"]),
                               ("ZREVRANGEBYLEX myzset [alpha [omega", [""])
                               ])

typeConnectionCommand = OrderedDict([("PING", ["PONG"]),
                                     # "QUIT":[],
                                     # "AUTH":[],
                                     ("ECHO hlc", ["hlc"]),
                                     ("SELECT 1", ["OK"])
                                     ])

typeServerCommand = OrderedDict([("FLUSHDB", ["OK"]),
                                 ("FLUSHALL", ["OK"]),
                                 ("CONFIG GET zset-max-ziplist-entries", ["zset-max-ziplist-entries", "128"]),
                                 ("CONFIG GET slowlog-log-slower-than", ["slowlog-log-slower-than", "10000"]),
                                 ("INFO", None),
                                 ("DBSIZE", ["0"]),
                                 ("RANDOMKEY", None),
                                 ("SET testServer_key 123", ["OK"]),
                                 ("MEMORY USAGE testServer_key", ["58"]),
                                 ("LATENCY HISTORY command", None)
                                 ])

typeScriptingCommand = OrderedDict([("EVAL \"return redis.call('set',KEYS[1],'bar')\" 1 foo", ["OK"]),
                                    (u"SCRIPT LOAD \"return 'hello moto'\"",
                                     ["232fd51614574cf0867b83d384a5e898cfd24e5a"]),
                                    ("EVALSHA \"232fd51614574cf0867b83d384a5e898cfd24e5a\" 0", ["hellomoto"]),
                                    ("SCRIPT EXISTS 232fd51614574cf0867b83d384a5e898cfd24e5a", ["1"]),
                                    ("SCRIPT FLUSH", ["OK"]),
                                    ("SCRIPT KILL", ["NOTBUSYNoscriptsinexecutionrightnow."]),
                                    ])

typeHyperLogLogCommand = OrderedDict([("PFADD databases \"Redis\" \"MongoDB\" \"MySQL\"", ["1"]),
                                      ("PFCOUNT databases", ["3"]),
                                      ("PFADD RDBMS \"MySQL\" \"MSSQL\" \"PostgreSQL\"", ["1"]),
                                      ("PFMERGE databases RDBMS", ["OK"]),
                                      ])

typeGeoCommand = OrderedDict([("GEOADD Sicily 13.361389 38.115556 Palermo 15.087269 37.502669 Catania", ["2"]),
                              ("GEORADIUS Sicily 15 37 100 km", ["Catania"]),
                              ("GEODIST Sicily Palermo Catania", ["166274.1516"]),
                              ("GEOADD Sicily 13.583333 37.316667 Agrigento", ["1"]),
                              ("GEORADIUSBYMEMBER Sicily Agrigento 100 km", ["Agrigento", "Palermo"]),
                              ("GEOHASH Sicily Palermo", ["sqc8b49rny0"]),
                              ("GEOPOS Sicily Palermo", ["13.36138933897018433", "38.11555639549629859"])
                              ])
