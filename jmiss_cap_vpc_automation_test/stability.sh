#!/bin/bash
if [ $# -lt 1 ]; then
	echo "ERROR: Parameter wrong"
        exit 1
fi
cd /export/Data/jmiss_auto_scripts/redis_stability_scripts/JCacheTest/jmiss_cap_vpc_automation_test

export PYTHONPATH=`pwd`
/usr/bin/python ./regression_cases/APIStabilityOfCap.py $1