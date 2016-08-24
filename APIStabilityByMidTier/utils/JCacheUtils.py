# coding=utf-8
import time

# from APIStabilityByMidTier.utils.tools import *


def CreateCluster(wc, ca):
    print "create cluster: start create cluster"
    status, headers, res_data = wc.create_cluster(ca)
    if status != 200:
        print "create cluster: send create request failed! status:[{0}]".format(status)
        return 1, None
    request_id = res_data['requestId']
    print "create cluster: send create request success! request_id={0}".format(request_id)
    # time.sleep(3)
    # status, headers, res_data = wc.get_cluster_id(request_id)
    # if status != 200:
    #     print "send create request failed! status:[{0}]".format(status)
    #     return 1, None
    # print res_data
    # resourceIds = res_data['resourceIds']
    # space_id = resourceIds[0]

    # get space info, check space status

    max_retry_time = 30
    retry_time = 0
    while retry_time <= max_retry_time:
        status, headers, res_data = wc.get_cluster_id(request_id)
        if status != 200:
            print "create cluster: send create request failed! status:[{0}]".format(status)
            return 1, None
        print res_data
        resourceIds = res_data['resourceIds']
        if resourceIds is not None:
            break
        # ins_status, capacity, password, flag, tenant_id, name, remarks = space
        print "create cluster: retry_time:{0}, creating cluster, requestId={1}".format(retry_time, request_id)
        retry_time += 1
        time.sleep(5)

    space_id = resourceIds[0]
    print "create cluster: send query cluster id request success! space_id={0}".format(space_id)
    status, headers, res_data = wc.get_cluster(space_id)
    cluster = res_data['cluster']
    if cluster is None:
        print "create cluster: get space:[{0}] status failed!".format(space_id)
        return 1, space_id
    ins_status = cluster['status']
    if ins_status != 100:
        print "create cluster: check cluster [{0}] status failed!".format(space_id)
        return 1, space_id
    print "create cluster:[{0}] success!".format(space_id)
    return 0, space_id


def CheckGetCluster(web_client, space_id):
    print "get cluster: start check get cluster"
    status, headers, res_data = web_client.get_cluster(space_id)
    if status != 200 or res_data['cluster'] is None:
        print "get cluster: get cluster request failed! status:[{0}]".format(status)
        return 1, None
    print "get cluster: get cluster request success!"
    ins_status = res_data['cluster']['status']
    if ins_status != 100:
        print "get cluster: check cluster [{0}] status failed!".format(space_id)
        return 1, space_id
    print "get cluster: [{0}] success".format(space_id)
    return 0, space_id


def CheckGetClusters(web_client, space_id):
    print "get clusters: start check get clusters"
    status, headers, res_data = web_client.get_clusters()
    if status != 200 or res_data['clusters'] is None:
        print "get clusters: get clusters request failed! status:[{0}]".format(status)
        return 1, None
    print "get clusters: get clusters request success!"
    for cluster in res_data['clusters']:
        if cluster['spaceId'] == space_id:
            break
    if cluster['spaceId'] != space_id or cluster['status'] != 100:
        print "get clusters: check cluster [{0}] status failed!".format(space_id)
        return 1, space_id
    print "get clusters success"
    return 0, space_id


def DeleteCluster(wc, space_id):
    print "delete cluster: start delete cluster"
    status, headers, res_data = wc.delete_cluster(space_id)
    if status != 200:
        print "delete cluster: send delete request failed! space_id:[{0}] status:[{1}]".format(space_id, status)
        return 1

    ins_status = 600
    max_retry_time = 30
    retry_time = 0
    while (ins_status == 600 or ins_status == 100) and retry_time <= max_retry_time:
        status, headers, res_data = wc.get_cluster(space_id)
        cluster = res_data['cluster']
        if cluster is None:
            break
        # ins_status, capacity, password, flag, tenant_id, name, remarks = space
        ins_status = cluster['status']
        print "delete cluster: retry_time:{0}, space:(status:{1}, capacity:{2}, name:{3}, remarks:{4})".format(retry_time, cluster['status'], cluster['capacity'], cluster['name'], cluster['remarks'])
        retry_time += 1
        time.sleep(5)
    if ins_status != 601 and cluster is not None:
        print "delete cluster: check cluster [{0}] status failed!".format(space_id)
        return 1
    print "delete cluster: test delete cluster:{0} success".format(space_id)
    return 0


def CheckAcl(wc, space_id):
    # test acl
    # local_ip = get_local_ip()
    # ips = [local_ip]
    print "check acl: start check acl"
    status, headers, res_data = wc.get_acl(space_id)
    if status != 200:
        print "check acl: get acl request failed! space_id:[{0}], status:[{1}], code:[{2}]".format(space_id, status,
                                                                                        res_data['code'])
        return 1
    # ips.sort()
    act_ips = res_data['acl']['ips']
    if act_ips is None:
        print "check acl: get acl failed, ips is null! space_id[{0}]".format(space_id)
        return 1
    print "check acl: current ips in acl is {0}".format(act_ips)
    # act_ips.sort()
    # if cmp(act_ips, ips) != 0:
    #     print "check acl: check acl failed!expected_ips:[{0}],actual_ips:[{1}]".format(ips, act_ips)
    #     return 1
    print "check acl: test check acl success"
    return 0
