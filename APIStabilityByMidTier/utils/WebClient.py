# coding=utf-8
import httplib
import json


class CreateArgs():
    def __init__(self, space_name="jcachetest", space_type=1, capacity=1, quantity=1, remarks="jcachetest", fee_type=1):
        self.args_str = "spaceName={0}&spaceType={1}&capacity={2}&quantity={3}&remarks={4}&feeType={5}" \
            .format(space_name, space_type, capacity, quantity, remarks, fee_type)

    def get_args_string(self):
        return self.args_str

    def set_capacity(self, capacity):
        self.args_str["capacity"] = capacity


class WebClient(object):
    def __init__(self, host, port, user, account, coupon_id):
        self.host = host
        self.port = port
        self.user = user
        self.account = account
        self.coupon_id = coupon_id

    def http_request(self, method, uri):
        hc = httplib.HTTPConnection(self.host, self.port)
        hc.request(method, "/{0}&user={1}&account={2}&dataCenter={3}".format(uri, self.user, self.account, "hb"))
        res = hc.getresponse()
        # print res.status
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def create_cluster(self, create_args):
        # 线上环境
        # return self.http_request("GET", "cache?action=createCacheCluster&{0}&coupons[0]=1015"
        #                                 "&discountId=&discountValue=".format(create_args.get_args_string()))
        # 测试环境
        return self.http_request("GET", "cache?action=createCacheCluster&{0}".format(create_args.get_args_string()))

    def pay_for_the_cluster(self, request_id):
        # 线上环境
        # return self.http_request("GET", "billing?action=pay&request_id={0}&coupons[0]=1015".format(request_id))
        # 测试环境
        return self.http_request("GET", "billing?action=pay&orderRequestId={0}".format(request_id))

    def get_cluster_id(self, request_id):
        return self.http_request("GET", "order?action=queryOrderStatus&orderRequest={0}".format(request_id))

    def delete_cluster(self, space_id):
        return self.http_request("GET", "cache?action=deleteCacheCluster&clusterId={0}".format(space_id))

    def get_clusters(self):
        return self.http_request("GET", "cache?action=queryCacheClusters")

    def get_cluster(self, space_id):
        return self.http_request("GET", "cache?action=queryCacheClusterDetail&clusterId={0}".format(space_id))

    def get_acl(self, space_id):
        return self.http_request("GET", "cache?action=queryCacheClusterAcl&clusterId={0}".format(space_id))

    # def set_acl(self, space_id, ips):
    #     acl = {"target": [space_id], "ips": ips, "action": "allow"}
    #     return self.http_request("PUT", "acl", json.dumps(acl))
    #
    # def del_acl(self, space_id, ips):
    #     acl = {"target": [space_id], "ips": ips, "action": "deny"}
    #     return self.http_request("PUT", "acl", json.dumps(acl))


