#!/bin/bash

Cmd="curl -s -m 3 -X GET http://xb8avfbqa212.cn-north-1.jdcloud-api.net/api/memcached?action=heartbeat"
CheckString="Healthy"
MaxTimes=3
LogDir="/export/Logs/memcached_read_write"
FileDate=`date '+%Y%m%d-%H%M%S'`
LogSaveDays=3

function writelog()
{
    time=`date +"%F %T.%N"`
    echo "[$time] [$$] $@" >> "${LogDir}/mc_rw_data_${FileDate}.log"
}

function check()
{
    retryTime=0
    while [ ${retryTime} -lt ${MaxTimes} ]; do
        curlResult=`${Cmd}`
        cmdResult=$?
        if [[ ${cmdResult} -eq 0 ]]; then
            break
        else
            writelog "${cmdResult}"
        fi
        ((mcRertyTime++))
        sleep 15
    done
    if [[ ${curlResult} =~ ${CheckString} && ${rertyTime} -lt ${MaxTimes} ]]; then
        echo "status:\"0\""
    elif [ ${rertyTime} -eq 3]; then
        echo "status:\"-1\",desc: ${cmdResult}"
    else
        echo "status:\"-1\",desc: ${curlResult}"
    fi
}


#clean up old log
function cleanLog()
{
    find ${LogDir} -mtime +${LogSaveDays} -name "mc_rw_data_*.log" -exec rm -rf {} \;
}

writelog "Heartbeat start"
check
cleanLog
writelog "Heartbeat result: ${curlResult}"
