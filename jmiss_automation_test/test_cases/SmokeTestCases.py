#!/usr/bin/python
# coding:utf-8

class SmokeTestCases:

    def test_create_an_instance(self, conf, instance_data):
        print "[SCENARIO] Create an instance including a master container and a slave container"
        #创建缓存云实例
        #查看缓存云实例详细信息
        #验证缓存云实例状态，status=100创建成功
        #查看缓存云实例详情，获取拓扑结构
        #获取CFS的拓扑结构

