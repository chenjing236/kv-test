import httplib
import json
class CreateArgs():
    def __init__(self, capacity=2097152, zoneid=1, remarks="jcachetest", space_name="jcachetest", space_type=1, quantity=1):
        self.args_dict = {"spaceName": space_name, "spaceType": space_type, "zoneId": zoneid, "capacity": capacity, "quantity": quantity,
         "remarks": remarks}

    def to_json_string(self):
        return json.dumps(self.args_dict)

    def set_capacity(self, capacity):
        self.args_dict["capacity"] = capacity


class WebClient(object):

    def __init__(self, host, md5_pin, auth_token):
        self.host = host
        self.md5_pin = md5_pin
        self.auth_token = auth_token

    def http_request(self, method, uri, data=None, version="v1.0"):
        hc = httplib.HTTPConnection(self.host)
        hc.request(method, "/{0}/{1}/{2}".format(version, self.md5_pin, uri), data, {"auth-Token": self.auth_token})
        res = hc.getresponse()
        status = res.status
        res_data = json.loads(res.read())
        headers = res.getheaders()
        hc.close()
        return status, headers, res_data

    def create_cluster(self, create_args):
        data = create_args.to_json_string()
        return self.http_request("POST", "clusters", data)

    def delete_cluster(self, space_id):
        return self.http_request("DELETE", "clusters/{0}".format(space_id))

    def set_acl(self,space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "allow"}
        return self.http_request("PUT", "acl", json.dumps(acl))

    def del_acl(self,space_id, ips):
        acl = {"target": [space_id], "ips": ips, "action": "deny"}
        return self.http_request("PUT", "acl", json.dumps(acl))

    def get_clusters(self):
        return self.http_request("GET", "clusters")

    def get_cluster(self,space_id):
        return self.http_request("GET", "clusters/{0}".format(space_id))

    def get_acl(self,space_id):
        return self.http_request("GET", "acl/{0}".format(space_id))



