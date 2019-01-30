#!/bin/bash

Cmd="curl -s -m 10 -X GET http://xb8avfbqa212.cn-north-1.jdcloud-api.net/api/memcached?action=heartbeat"
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
        ((retryTime++))
        sleep 10
    done
    if [[ ${curlResult} =~ ${CheckString} && ${retryTime} -lt ${MaxTimes} ]]; then
        echo "status:\"0\""
        writelog "Heartbeat result: ${curlResult}"
    elif [ ${retryTime} -eq 3]; then
        echo "status:\"-1\",desc: Connection time out, error code: ${cmdResult}"
        writelog "Connection time out, error code: ${cmdResult}"
    else
        echo "status:\"-1\",desc: ${curlResult}"
        writelog "${curlResult}"
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

