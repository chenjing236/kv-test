import time


def CreateCluster(wc, ca, sql_c):
    status, headers, res_data = wc.create_cluster(ca)
    if status != 200 or res_data['code'] != 1:
        print "send create request failed! status:[{0}], code:[{1}]".format(status, res_data['code'])
        return 1, None
    space_id = res_data['attach']
    print "send create request successed! space_id{0}".format(space_id)

    # get space info, check space status

    ins_status = 0
    max_retry_time = 30
    retry_time = 0
    while ins_status == 0 and retry_time <= max_retry_time:
        space = sql_c.get_space_status(space_id)
        if space is None:
            print "CREATE: get space:[{0}] status failed!".format(space_id)
            return 1, space_id
        ins_status, capacity, password, flag, tenant_id, name, remarks = space
        print "retry_time:{0}, space:{1}".format(retry_time, space)
        retry_time += 1
        time.sleep(5)

    if ins_status != 100:
        print "create cluster: check cluster [{0}] status failed!".format(space_id)
        return 1, space_id
    print "create cluster:[{0}] success!".format(space_id)
    return 0, space_id


def DeleteCluster(wc, space_id, sql_c):
    status, headers, res_data = wc.delete_cluster(space_id)
    if status != 200 or res_data['code'] != 1:
        print "send delete request failed! space_id:[{0}] status:[{1}], code:[{2}]".format(space_id, status,
                                                                                           res_data['code'])
        return 1

    ins_status = 600
    max_retry_time = 30
    retry_time = 0
    while ins_status == 600 and retry_time <= max_retry_time:
        space = sql_c.get_space_status(space_id)
        if space is None:
            print "DELETE: get space:[{0}] status failed!".format(space_id)
            return 1
        ins_status, capacity, password, flag, tenant_id, name, remarks = space
        print "retry_time:{0}, space:{1}".format(retry_time, space)
        retry_time += 1
        time.sleep(5)
    if ins_status != 601:
        print "delete cluster: check cluster [{0}] status failed!".format(space_id)
        return 1
    print "test delete cluster:{0} success".format(space_id)
    return 0


def SetAcl(wc, space_id, sql_c, ips):
    status, headers, res_data = wc.set_acl(space_id, ips)
    if status != 200 or res_data['code'] != 1:
        print "set acl request failed! space_id:[{0}], status:[{1}], code:[{2}]".format(space_id, status,
                                                                                        res_data['code'])
        return 1
    status, headers, res_data = wc.get_acl(space_id)
    if status != 200 or res_data['code'] != 1:
        print "get acl request failed! space_id:[{0}], status:[{1}], code:[{2}]".format(space_id, status,
                                                                                        res_data['code'])
        return 1
    ips.sort()
    if 'attach' not in res_data or 'ips' not in res_data['attach']:
        print "get acl failed! space_id[{0}]".format(space_id)
        return 1
    act_ips = res_data['attach']['ips']
    act_ips.sort()
    if cmp(act_ips, ips) != 0:
        print "check acl failed!expected_ips:[{0}],actual_ips:[{1}]".format(ips, act_ips)
        return 1
    return 0
