#!/bin/bash
if [ $# -lt 1 ]; then
	echo "ERROR: Parameter wrong"
        exit 1
fi
cd /export/Data/jmiss_auto_scripts/redis_stability_scripts_$1/JCacheTest/jmiss_cap_redis_api_test

export PYTHONPATH=`pwd`:/export/Data/jmiss_auto_scripts/redis_stability_scripts_$1/jcloud-sdk-python/
/usr/bin/python ./regression_cases/APIStabilityOfCap.py $1