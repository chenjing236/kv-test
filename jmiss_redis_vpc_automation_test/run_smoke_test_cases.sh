#!/bin/bash
if [ $# -lt 1 ];then
        echo "[WARNING] Please input sleep time"
        exit 0
fi
# current path
current_path=`pwd`
wait_time=$1
# list of test cases
test_cases_list=`ls -l ${current_path}/test_cases | grep 'SmokeTestCases' | awk '{print $NF}'`
for line in ${test_cases_list}
do
	python -m pytest -v ./test_cases/$line -s -v --config ./config/conf_test_int_v2.json --data ./data/instance_data.json
	sleep ${wait_time}
done
