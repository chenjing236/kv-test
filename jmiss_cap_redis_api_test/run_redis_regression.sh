#!/bin/bash
if [ $# -lt 1 ];then
        echo "[WARNING] Please input sleep time"
        exit 0
fi
# current path
current_path=`pwd`
wait_time=$1
# list of test cases
test_cases_list=`ls -l ${current_path}/regression_cases/redis_cases/ | grep 'test_' | awk '{print $NF}'`

for line in ${test_cases_list}
do
	python -m pytest -v ./regression_cases/redis_cases/$line -s -v --config ./config/redis_config/config_test.json --data ./data/redis_data/data_test.json
	sleep ${wait_time}
done
