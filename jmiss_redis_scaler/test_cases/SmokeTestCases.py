# coding:utf-8
from utils.HttpClient import *
from utils.SQLClient import *
from steps.ClusterOperation import *


def upgrade_cluster_ap():
    with open("../config/conf_test_02.json", 'r') as load_f:
        config = json.load(load_f)
    http_client = HttpClient(config["host"])
    sql_client = SQLClient(config["mysql_host"], config["mysql_port"], config["mysql_user"], config["mysql_passwd"], config["mysql_db"])
    cluster = Cluster(http_client, sql_client, config)
    upgrade_ap_step(cluster, "redis-4notrtjmp4")
    get_operation_result_step(cluster, "redis-4notrtjmp4")


def upgrade_all_cluster_ap():
    with open("../config/conf_test_02.json", 'r') as load_f:
        config = json.load(load_f)
    http_client = HttpClient(config["host"])
    sql_client = SQLClient(config["mysql_host"], config["mysql_port"], config["mysql_user"], config["mysql_passwd"], config["mysql_db"])
    cluster = Cluster(http_client, sql_client, config)
    f = open("../config/space_id", 'r')
    space_id = f.readline().replace('\n', '')
    while space_id:
        upgrade_ap_step(cluster, space_id)
        get_operation_result_step(cluster, space_id)
        space_id = f.readline().replace('\n', '')
    f.close()

if __name__ == '__main__':
    upgrade_all_cluster_ap()
