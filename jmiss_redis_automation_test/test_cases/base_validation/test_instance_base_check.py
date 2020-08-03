from jmiss_redis_automation_test.steps.InstanceOperation import *
from jmiss_redis_automation_test.steps.FusionOpertation import *
from jmiss_redis_automation_test.steps.Valification import *
from jmiss_redis_automation_test.utils.SQLClient import *

class TestInstanceBasecheck:
    def __get_sql_conn(self, config):
        sql_conn = SQLClient(config["mysql_host"], config["mysql_port"], config["mysql_user"],
                             config["mysql_passwd"], config["mysql_db"])
        return sql_conn
    
    def __get_password(self, config, instance_id):
        sql_conn = self.__get_sql_conn(config)
        sql = "select password from instance where instance_id='%s'" % instance_id
        password = sql_conn.exec_query_one(sql)
        return password

    def __get_flavor_class(self, config, instance_id):
        sql_conn = self.__get_sql_conn(config)
        sql = "select flavor_class from instance where instance_id='%s'" % instance_id
        flavor_class = sql_conn.exec_query_one(sql)
        return flavor_class

    def __check_basic_validation(self, config, expected_data, instance_id, password, flavor_class):
        expected_object = baseCheckPoint(expected_data['%s' % flavor_class], password)
        result = check_admin_proxy_redis_configmap(instance_id, config, expected_object, 1)

        return result

    @pytest.mark.basecheck
    def test_standard_base_check(self, config, instance_data, expected_data, instance_id):
        instance_id = instance_id
        password = self.__get_password(config, instance_id)
        flavor_class = self.__get_flavor_class(config, instance_id)

        assert self.__check_basic_validation(config, expected_data, instance_id, '%s' % password,
                                             flavor_class)

    @pytest.mark.reset
    def test_modifySpecifedInstanceClass(self, config):
        resp = reset_class(config, "redis-24hu7ri9yx85", 'redis.s.small.basic', None, 2)
        assertRespNotNone(resp)
        instance = query_instance_recurrent(300, 6, "redis-24hu7ri9yx85", config, None)

    @pytest.mark.allbasecheck
    def test_all_instances_base_check(self, config, instance_data, expected_data):
        region = config["region"]
        sql_conn = self.__get_sql_conn(config)
        flavor_sql = "select flavor_class from instance where status!='deleted' and status!='error'" \
                     "and status!='deleting'group by flavor_class order by flavor_class"
        flavors = sql_conn.exec_query_all(flavor_sql)
        for flavor in flavors:
            print("=================================================")
            print('flavor class is %s' % flavor[0])

            if flavor[0] not in "redis.m.medium.basic":
                sql = "select instance_id, password from instance where status!='deleted' and status!='error'" \
                      "and status!='deleting' and region_id='%s' and flavor_class='%s';" % (region, flavor[0])
                #print("sql is %s" % sql)
                instances = sql_conn.exec_query_all(sql)
                if instances is not None:
                    for instance in instances:
                        password = instance[1]
                        print('instance is %s, password is %s' % (instance[0], password))
                        #if str(instance[0]) not in 'redis-gri0m4a6ty7o':
                        self.__check_basic_validation(config, expected_data, instance[0], password, flavor)
