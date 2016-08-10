import time


def CreateCluster(wc, ca, sql_c):
    status, headers, res_data = wc.create_cluster(ca)
    assert status == 200
    assert res_data['code'] == 1
    space_id = res_data['attach']
    print res_data
    print "send create request successed! space_id{0}".format(space_id)

    space = sql_c.get_space_status(space_id)
    assert space is not None
    ins_status, capacity, token, flag, tenant_id, name, remarks = space
    assert ins_status == 0 or ins_status == 100
    max_retry_time = 30
    retry_time = 0
    while ins_status == 0 and retry_time <= max_retry_time:
        time.sleep(5)
        space = sql_c.get_space_status(space_id)
        assert space is not None
        ins_status, capacity, token, flag, tenant_id, name, remarks = space
        print "retry_time:{0}, space:{1}".format(retry_time, space)
        retry_time += 1

    assert ins_status == 100
    print "create cluster success!"
    return space_id, space


def DeleteCluster(wc, space_id, sql_c):
    status, headers, res_data = wc.delete_cluster(space_id)
    assert status == 200
    assert res_data['code'] == 1

    ins_status = 600
    max_retry_time = 30
    retry_time = 0
    while ins_status == 600 and retry_time <= max_retry_time:
        space = sql_c.get_space_status(space_id)
        assert space is not None
        ins_status, capacity, token, flag, tenant_id, name, remarks = space
        print "retry_time:{0}, space:{1}".format(retry_time, space)
        retry_time += 1
        time.sleep(5)
    assert ins_status == 601
    print "test delete cluster:{0} success".format(space_id)


def CompareInstance(jinstance, jinstance_expect, space_id):
    ip, port, copy_id, flag = jinstance_expect
    assert jinstance['ip'] == ip
    assert jinstance['port'] == port
    assert jinstance['copyId'] == copy_id
    assert jinstance['flag'] == flag
    assert jinstance['spaceId'] == space_id


def CheckClusterInfo(self, cluster, space, instances, space_id, domian):
    status, capacity, password, flag, tenant_id, name, remarks = space
    assert cluster['status'] == status
    assert cluster['flag'] == flag
    assert cluster['capacity'] == capacity
    assert cluster['password'] == password
    assert cluster['tenantId'] == tenant_id
    assert cluster['name'] == name
    assert cluster['remarks'] == remarks
    assert cluster['spaceId'] == space_id
    assert cluster['domain'] == domian
    jinstance = cluster['instances']
    assert len(jinstance) == 2
    if jinstance[0]['copyId'] != 'm':
        tmp = jinstance[0]
        jinstance[0] = jinstance[1]
        jinstance[1] = tmp
    self.CompareInstance(jinstance[0], instances[0], space_id)
    self.CompareInstance(jinstance[1], instances[1], space_id)