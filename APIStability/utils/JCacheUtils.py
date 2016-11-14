import time
import logging.config

logging.config.fileConfig('logging.conf')
info_logger = logging.getLogger(__name__)
# info_logger.setLevel(logging.DEBUG)

failure_logger = logging.getLogger('failure.test_jmiss_api')
# failure_logger.setLevel(logging.WARNING)

stat_logger = logging.getLogger('stat.test_jmiss_api')
# stat_logger.setLevel(logging.INFO)


def CreateCluster(wc, ca, sql_c):
    info_logger.info("create cluster: start create cluster")
    status, headers, res_data = wc.create_cluster(ca)
    if status != 200 or res_data['code'] != 0:
        info_logger.error("create cluster: send create request failed! status:[{0}], code:[{1}]".format(status, res_data['code']))
        return 1, None
    space_id = res_data['attach']['spaceId']
    info_logger.info("create cluster: send create request success! space_id[{0}]".format(space_id))

    # get space info, check space status

    ins_status = 200
    max_retry_time = 30
    retry_time = 0
    while ins_status == 200 and retry_time <= max_retry_time:
        space = sql_c.get_space_status(space_id)
        if space is None:
            info_logger.error("create cluster: get space:[{0}] status failed!".format(space_id))
            return 1, space_id
        ins_status, capacity, password, cluster_type, tenant_id, name, remarks = space
        info_logger.debug("create cluster: retry_time:{0}, space:{1}".format(retry_time, space))
        retry_time += 1
        time.sleep(5)

    if ins_status != 100:
        info_logger.error("create cluster: check cluster [{0}] status failed!".format(space_id))
        return 1, space_id
    info_logger.info("create cluster: test create cluster [{0}] success!".format(space_id))
    return 0, space_id


def CheckGetCluster(web_client, space_id):
    info_logger.info("get cluster: start check get cluster")
    status, headers, res_data = web_client.get_cluster(space_id)
    if status != 200 or res_data['attach'] is None:
        info_logger.error("get cluster: get cluster request failed! status:[{0}]".format(status))
        return 1, None, None
    info_logger.info("get cluster: get cluster request success!")
    ins_status = res_data['attach']['status']
    instances = res_data['attach']['shards'][0]['instances']
    if ins_status != 100:
        info_logger.error("get cluster: check cluster [{0}] status failed!".format(space_id))
        return 1, space_id, None
    info_logger.info("get cluster: test get cluster [{0}] success".format(space_id))
    return 0, space_id, instances


def CheckGetClusters(web_client, space_id):
    info_logger.info("get clusters: start check get clusters")
    status, headers, res_data = web_client.get_clusters()
    if status != 200 or res_data['attach'] is None:
        info_logger.error("get clusters: get clusters request failed! status:[{0}]".format(status))
        return 1, None
    info_logger.info("get clusters: get clusters request success!")
    for cluster in res_data['attach']:
        if cluster['spaceId'] == space_id:
            break
    if cluster['spaceId'] != space_id or cluster['status'] != 100:
        info_logger.error("get clusters: check cluster [{0}] status failed!".format(space_id))
        return 1, space_id
    info_logger.info("get clusters: test get clusters success")
    return 0, space_id


def DeleteCluster(wc, space_id, sql_c):
    info_logger.info("delete cluster: start delete cluster")
    status, headers, res_data = wc.delete_cluster(space_id)
    if status != 200 or res_data['code'] != 0:
        info_logger.error("send delete request failed! space_id:[{0}] status:[{1}], code:[{2}]".format(space_id, status,
                                                                                           res_data['code']))
        return 1

    ins_status = 600
    max_retry_time = 30
    retry_time = 0
    while ins_status == 600 and retry_time <= max_retry_time:
        space = sql_c.get_space_status(space_id)
        if space is None:
            info_logger.error("delete cluster: get space:[{0}] status failed!".format(space_id))
            return 1
        ins_status, capacity, password, cluster_type, tenant_id, name, remarks = space
        info_logger.debug("delete cluster: retry_time:{0}, space:{1}".format(retry_time, space))
        retry_time += 1
        time.sleep(5)
    if ins_status != 101:
        info_logger.error("delete cluster: check cluster [{0}] status failed! status={1}".format(space_id, ins_status))
        return 1
    info_logger.info("delete cluster: test delete cluster:{0} success".format(space_id))
    return 0


def SetAcl(wc, space_id, sql_c, ips):
    status, headers, res_data = wc.set_acl(space_id, ips)
    if status != 200 or res_data['code'] != 0:
        info_logger.error("check acl: set acl request failed! space_id:[{0}], status:[{1}], code:[{2}]".format(space_id, status,
                                                                                        res_data['code']))
        return 1
    info_logger.info("check acl: set acl request success! space_id:[{0}]".format(space_id))
    status, headers, res_data = wc.get_acl(space_id)
    if status != 200 or res_data['code'] != 0:
        info_logger.error("check acl: get acl request failed! space_id:[{0}], status:[{1}], code:[{2}]".format(space_id, status,
                                                                                        res_data['code']))
        return 1
    ips.sort()
    if 'attach' not in res_data or 'ips' not in res_data['attach']:
        info_logger.error("check acl: get acl failed! space_id[{0}]".format(space_id))
        return 1
    info_logger.info("check acl: get acl request success! ips:[{0}]".format(ips))
    act_ips = res_data['attach']['ips']
    act_ips.sort()
    if cmp(act_ips, ips) != 0:
        info_logger.error("check acl: check acl failed!expected_ips:[{0}],actual_ips:[{1}]".format(ips, act_ips))
        return 1
    info_logger.info("check acl: check acl success! actual_ips:[{0}]".format(act_ips))
    return 0
