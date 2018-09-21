import pytest
import time
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.memcached.client.MemcachedClient import MemcachedClient
from jdcloud_sdk.services.memcached.apis.CreateInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.DeleteInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.DescribeInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.DescribeInstancesRequest import *
from jdcloud_sdk.services.memcached.apis.FlushInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.ModifyInstanceRequest import *
from jdcloud_sdk.services.memcached.apis.ModifyInstanceSpecRequest import *
from jdcloud_sdk.services.memcached.models.Instance import *
from jdcloud_sdk.services.memcached.models.InstanceSpec import *
from jdcloud_sdk.services.charge.models.ChargeSpec import *
from jdcloud_sdk.services.common.models.Sort import *
from jdcloud_sdk.services.charge.models.Charge import *
from jdcloud_sdk.services.common.models.Filter import Filter
from copy import deepcopy



class TestOpenAPI:
    def getDate(self):
        check_data = {
            "azId": "cn-north-1a"
            , "instanceStatus": "running"
            , "instanceType": "single"
            , "mcVersion": "1.5.8"
            , "port": 11211
            , "subnetId": "subnet-rdwzhqpvvr"
            , "vpcId": "vpc-hc363aao5w"
        }
        exist_data = {
            "createTime": ""
            , "domain": ""
            , "instanceId": ""
            , "usedMemoryMB": ""
            , "charge": ""
        }
        change_data = {
            "instanceClass": "MC-S-1C1G"
            , "instanceDescription": "desc"
            , "instanceName": "auto_test"
            , "mcAuth": True
        }
        return check_data, exist_data, change_data

    @pytest.fixture(scope='function')
    def setClient(self):
        # access_key = "824D3298D39F5DA6AE0E082DC06159D5"
        # secret_key = "14565AF4C9847E4EA43D89BA2A9E0EAD"
        access_key = "BDA9C74FF12818DFDC8463C16FB884B2"
        secret_key = "A2188C6C9EC959289901369503E8E0F7"
        credential = Credential(access_key, secret_key)
        # config = Config("apigw-test.openapi.jdcloud.com", SCHEME_HTTP)
        config = Config("192.168.182.82:8000", SCHEME_HTTP)
        # config = Config("192.168.244.73:8080", SCHEME_HTTP)
        client = MemcachedClient(credential, config)
        request_id = "req-" + str(time.time())
        header = {'x-jdcloud-pin': 'jcloud_00', "x-jdcloud-request-id": request_id}

        return client, header

    @pytest.mark.openapi
    def test_describeInstance(self, setClient):
        self.describeInstance("mc-38asdqfrhx")
        print "========================"

    @pytest.mark.openapi
    def test_describeInstances(self, setClient):
        client, header = setClient
        try:
            parameters = DescribeInstancesParameters('cn-north-1')
            parameters.setPageNumber(2)
            parameters.setPageSize(11)
            filter1 = Filter('instanceName', '', 'eq')
            filter2 = Filter('instanceStatus', 'running')
            sort = Sort('createTime', 'desc')
            # parameters.setSorts([sort])
            # parameters.setFilters([filter1, filter2])
            request = DescribeInstancesRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "------------describeInstances--------------"
            print resp.result
            print "--------------------------"
            for i in resp.result['instances']:
                print i['instanceId']
        except Exception, e:
            print e


    @pytest.mark.openapi
    def test_createInstance(self, setClient):
        client, header = setClient
        try:
            charge = ChargeSpec('prepaid_by_duration', 'year', 1)
            instance = InstanceSpec('MC-S-1C1G', 'single', 'cn-north-1a',
                                    'vpc-hc363aao5w', 'subnet-rdwzhqpvvr', "auto_test", '1.5.8', False, charge, "desc")

            parameters = CreateInstanceParameters('cn-north-1', instance)
            request = CreateInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "------------createInstance--------------"
            print resp.result
            print "--------------------------"
        except Exception, e:
            print e



    @pytest.mark.openapi
    def test_deleteInstances(self, setClient):
        client, header = setClient
        instance_id = "mc-lb0q9yp46s"
        try:
            parameters = DeleteInstanceParameters('cn-north-1',instance_id)
            request = DeleteInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "------------deleteInstances--------------"
            print resp.result
        except Exception, e:
            print e

    @pytest.mark.openapi
    def test_flushInstances(self, setClient):
        client, header = setClient
        try:
            parameters = FlushInstanceParameters('cn-north-1', "mc-r9y0r4miq8")
            request = FlushInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "---------test_flushInstances----------"
            print resp.result
        except Exception, e:
            print e

    @pytest.mark.openapi
    def test_modifyInstances(self, setClient):
        client, header = setClient
        try:
            parameters = ModifyInstanceParameters('cn-north-1', "mc-38asdqfrhx")
            parameters.setInstanceName("new_auto_test")
            parameters.setInstanceDescription("new_desc")
            parameters.setMcAuth(True)
            # parameters.setMcPswd()
            request = ModifyInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "-------------test_modifyInstances--------------"
            print resp.result
        except Exception, e:
            print e


    @pytest.mark.openapi
    def test_modifyInstanceSpec(self, setClient):
        client, header = setClient

        try:
            parameters = ModifyInstanceSpecParameters('cn-north-1', "mc-38asdqfrhx")
            parameters.setInstanceClass('MC-S-1C2G')
            request = ModifyInstanceSpecRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "-----------modifyInstanceSpe--------------"
            print resp.result
        except Exception, e:
            print e

    def describeInstance(self, instance_id, c_data=None):
        client, header = self.setClient()
        check_data, exist_data, change_data = self.getDate()
        if c_data is not None:
            change_data = c_data
        try:
            parameters = DescribeInstanceParameters('cn-north-1', instance_id)
            request = DescribeInstanceRequest(parameters, header)
            resp = client.send(request)
            if resp.error is not None:
                print resp.error.code, resp.error.message
            print "-----------------"
            print resp.result
            print "-----------------"
            for k, y in check_data.items():
                if k in resp.result['instance']:
                    if resp.result['instance'][k] != y:
                        print k,y
                else:
                    print k,y
            for k, y in exist_data.items():
                # assert k in resp.result['instance']
                if k not in resp.result['instance']:
                    print k,y
            for k, y in change_data.items():
                # assert resp.result['instance'][k] == y
                if k in resp.result['instance']:
                    if resp.result['instance'][k] != y:
                        print k,y
                else:
                    print k,y
        except Exception, e:
            print e


    def wait(self, wait_count, wait_time, func, args):
        while wait_count > 0:
            func(args)
            time.sleep(wait_time)


    def validateResult(self, result, data):
        if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
            print "type error"
            return
        for k,y in data.items():
            if k in result:
                if result[k] != y:
                    print k, y
            else:
                print k, y

    def existResult(self, result, data):
        if type(data).__name__ != 'dict' or type(result).__name__ != 'dict':
            print "type error"
            return
        for k, y in data.items():
            if k not in result:
                print k, y
