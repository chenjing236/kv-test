#!/bin/bash

cd /export/Data/jmiss_auto_scripts/memcached_stability_scripts/JCacheTest/jmiss_memcached_vpc_automation_test

date=`date '+%Y%m%d-%H%M%S'`
pytest ./test_cases/openapi_cases -s -v -m openapi --config ./config/conf_hb.json --data ./data/instance_data_hb.json > /export/Logs/mc_stability_test/mc_stability_$date.log 2>&1

cases=(
'createInstance'
'describeInstance'
'describeInstanceNotFound'
'describeInstances'
'flushInstance'
'flushInstanceNotFound'
'modifyInstance'
'modifyInstanceWithoutAuth'
'modifyInstanceSpec'
)
re=`cat /export/Logs/mc_stability_test/mc_stability_${date}.log|grep -E 'PASSED|FAILED'`
i=0
for ca in ${re[@]}; do
        if [[ $ca =~ 'PASSED' ]]; then
                echo "mc.${cases[$i]}.status:\"0\""
        else
                if [ $i -eq 0 ]; then
                    echo "mc.${cases[$i]}.status:\"failed\""
                    break
                fi
                echo "mc.${cases[$i]}.status:\"failed\""
        fi
        ((i++))
done

#clean up old log
cd /export/Logs/mc_stability_test
day=`date -d "2 days ago" +%Y%m%d`
ls *${day}*.log |xargs \rm -f

