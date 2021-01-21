#!/bin/bash

#clean up old log
cd /export/Logs/redis28_stability_test_new
day=`date -d "2 days ago" +%Y%m%d`
ls *${day}*.log |xargs \rm -f

#todo need to be updated
cd /home/chenjing/kv-test/jmiss_redis28_automation_test

date=`date '+%Y%m%d-%H%M%S'`
pytest -s -v --config ./config/conf_hb.json --data ./data/data_hb.json -m smoke > /export/Logs/redis28_stability_test_new/redis28_stability_$date.log 2>&1

cases=(
'BackupRestore'
'ModifyConfig'
'QueryConfig'
'QueryListFilter'
'ResetPassword'
'ResizeInstance'
'UpdateMeta'
)
re=`cat /export/Logs/redis28_stability_test_new/redis28_stability_${date}.log|grep -E 'PASSED|FAILED$'`
i=0
for ca in ${re[@]}; do
        if [[ $ca =~ 'PASSED' ]]; then
                echo "redis28.${cases[$i]}.status:\"0\""
        else
                if [ $i -eq 0 ]; then
                    echo "redis28.${cases[$i]}.status:\"failed\""
                    break
                fi
                echo "redis28.${cases[$i]}.status:\"failed\""
        fi
        ((i++))
done

