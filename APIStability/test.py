# coding=utf-8
import sys
import httplib
import json

def main(argv):
    hc = httplib.HTTPConnection("192.168.172.33", 80)
    f = open("C:\Users\Administrator\Desktop\invalid domains.txt", "r")
    while True:
        line = f.readline()
        if line:
            pass  # do something here
            line = line.strip()
            p = line.rfind('com')
            domain = line[0:p + 3]
            print domain
            data = "[{\"domain\":\"" + domain + "\",\"records\":[]}]"
            hc.request("POST", "/dns/pub/update", data)
            res = hc.getresponse()
            status = res.status
            res_data = json.loads(res.read())
            # headers = res.getheaders()
            hc.close()
            print status
            print res_data
            # print headers
        else:
            break
    f.close()

if __name__ == "__main__":
    main(sys.argv)
