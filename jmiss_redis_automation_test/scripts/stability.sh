#!/bin/bash

#clean up old log
cd /export/Logs/redis40_stability_test
day=`date -d "2 days ago" +%Y%m%d`
if [ -f *${day}*.log ]; then
        ls *${day}*.log |xargs \rm -f
fi

cd /export/Data/jmiss_auto_scripts/memcached_stability_scripts/JCacheTest/jmiss_redis_automation_test

date=`date '+%Y%m%d-%H%M%S'`
pytest --config ./config/conf_pro.json -m smoke > /export/Logs/redis40_stability_test/redis40_stability_$date.log 2>&1

cases=(
'createInstance'
'describeInstance'
'describeInstances'
'modifyCacheInstanceAttribute'
'modifyCacheInstanceClass'
'modifyInstanceConfig'
'resetCacheInstancePassword'
)
re=`cat /export/Logs/redis40_stability_test/redis40_stability_${date}.log|grep -E 'PASSED|FAILED$'`
i=0
for ca in ${re[@]}; do
        if [[ $ca =~ 'PASSED' ]]; then
                echo "redis40.${cases[$i]}.status:\"0\""
        else
                if [ $i -eq 0 ]; then
                    echo "redis40.${cases[$i]}.status:\"failed\""
                    break
                fi
                echo "redis40.${cases[$i]}.status:\"failed\""
        fi
        ((i++))
done
