#!/bin/bash

cd /export/Data/jmiss_auto_scripts/memcached_stability_scripts/JCacheTest/jmiss_memcached_vpc_automation_test

date=`date '+%Y%m%d-%H%M%S'`
pytest ./test_cases/openapi_cases -s -v -m openapi --config ./config/conf_hb.json --data ./data/instance_data_hb.json > /export/Logs/mc_stability_test/mc_stability_$date.log 2>&1

cases=(
'createInstance Failed'
'describeInstance Failed'
'describeInstanceNotFound Failed'
'describeInstances Failed'
'flushInstance Failed'
'flushInstanceNotFound Failed'
'modifyInstance Failed'
'modifyInstanceWithoutAuth Failed'
'modifyInstanceSpec Failed'
)
re=`cat /export/Logs/mc_stability_test/mc_stability_${date}.log|grep -E 'PASSED|FAILED'`
i=0
for ca in ${re[@]}; do
        if [[ $ca =~ 'PASSED' ]]; then
                echo "mc.stab$i.status:0"
        else
                echo "mc.stab$i.status:"${cases[$i]}
        fi
        ((i++))
done

