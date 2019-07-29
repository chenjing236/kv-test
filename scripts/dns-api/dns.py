#!/bin/bash
# code=utf-8

import time
import hashlib
import json


now = int(time.time())
timeStr = time.strftime("%H%M%Y%m%d")
print now
print timeStr

appCode = "jmiss-redis"
erp = "haojinglong"
businessId = "928340688987c061edf755fc42ab613e"

signStr = erp + "#" + businessId + "NP" + timeStr
hmd5 = hashlib.md5()
hmd5.update(signStr)
sign = hmd5.hexdigest()
url = "api-np.jcloud.com"
domain = "jredis-cn-north-1-prod-redis-test3sbnkp.jdcloud.com"
print sign

data_reserve = {"domain": domain,
        "primary": "jcloud",
        "project_name": "jmiss-redis",
        "manage_erp": "haojinglong",
        "network": 1}

data_resolution = {"domain": domain,
                   "data": [{"type": "A", "records": ["10.207.67.216"]}]}

domain_check = "curl -H \"\"Content-type:application/json\"\" -H \"appCode:{0}\" " \
       "-H \"erp:{1}\" -H \"timestamp:{2}\" -H \"sign:{3}\" " \
       "http://{4}/V1/Dns/domainCheck?domain={5}".format(appCode, erp, now, sign, url, domain)

reserve = "curl -XPOST -H \"\"Content-type:application/json\"\" -H \"appCode:{0}\" " \
       "-H \"erp:{1}\" -H \"timestamp:{2}\" -H \"sign:{3}\" " \
       "-d \'{4}\' " \
       "http://{5}/V1/Dns/reserve".format(appCode, erp, now, sign, json.dumps(data_reserve), url)

resolution = "curl -XPOST -H \"\"Content-type:application/json\"\" -H \"appCode:{0}\" " \
       "-H \"erp:{1}\" -H \"timestamp:{2}\" -H \"sign:{3}\" " \
       "-d \'{4}\' " \
       "http://{5}/V1/Dns/resolution".format(appCode, erp, now, sign, json.dumps(data_resolution), url)

del_domain = "curl -H \"\"Content-type:application/json\"\" -H \"appCode:{0}\" " \
       "-H \"erp:{1}\" -H \"timestamp:{2}\" -H \"sign:{3}\" " \
       "http://{4}/V1/Dns/delDomain?domain={5}".format(appCode, erp, now, sign, url, domain)

print domain_check
print reserve
print resolution
print del_domain
