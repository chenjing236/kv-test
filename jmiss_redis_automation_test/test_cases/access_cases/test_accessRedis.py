import pytest
import requests
import json
# from redis import StrictRedis
from jmiss_redis_automation_test.utils.SqlConst import *



class TestAccessRedis:

    @pytest.mark.access
    # @pytest.mark.openapi
    # def test_access(self, init_instance, config):
    def test_access(self, config):
        # print sql_const.QUERY_INSTANCE
        # client, resp, instance_id = init_instance
        instance_id = "redis-ct2lfgr96qo3"
        assert instance_id is not None
        host = self.getInstanceNlb(instance_id)
        # client = StrictRedis(host=host, port=6379, db=0, password=config["instance_password"])
        # client = StrictRedis(host=host, port=6379, db=0)
        # assert client.set("test", "abc")
        # assert client.get("test") == "abc"
        # client.execute_command()


    def getInstanceNlb(sefl, instance_id):
        url = "http://10.226.134.46:18810/resource/all/topology/" + instance_id
        r = requests.get(url)
        data = r.json()["data"]["children"][3]["children"][0]["info"]
        print data
        info = json.loads(data)
        return info["status"]["expose_domain"]








