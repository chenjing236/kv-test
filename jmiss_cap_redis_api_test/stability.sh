#!/bin/bash
if [ $# -lt 1 ]; then
	echo "ERROR: Parameter wrong"
        exit 1
fi
cd /export/Data/jmiss_auto_scripts/redis_stability_scripts_$1/JCacheTest/jmiss_cap_redis_api_test

export PYTHONPATH=`pwd`:/export/Data/jmiss_auto_scripts/redis_stability_scripts_$1/jcloud-sdk-python/
date=`date '+%Y%m%d-%H%M%S'`
/usr/bin/python ./regression_cases/APIStabilityOfCap.py $1 > /export/Logs/redis_stability_test/redis_stability_$date.log 2>&1
cat /export/Logs/redis_stability_test/redis_stability_$date.log | tail -n 8

# clean up old log
today=`date '+%Y%m%d-%H%M%S' | awk -F'-' '{print $1}'`
cd /export/Logs/redis_stability_test/
ls | awk -v today=$today -F'-|_' '{if($3 < today-1) {print}}' | xargs \rm -f