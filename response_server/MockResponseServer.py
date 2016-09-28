#!/usr/bin/env python
# encoding: utf-8
import BaseHTTPServer
import json

class TestHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    RESPONSE = None
    RESPONSE_CODE = 200
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if self.path == "/getCluster":
            self.send_response(200)
            #data="\r\n{\"code\":0,\"message\":\"get cluster\"}"
            data="{\"code\":0,\"message\":\"get cluster\"}"
        else:
            self.send_response(404,"Incorrect request uri")
            #data = "\r\n{\"code\":1,\"message\":\"URI is incorrect\"}"
            data = "{\"code\":1,\"message\":\"URI is incorrect\"}"

        self.wfile.write(data)

    def do_POST(self):
        length = self.headers.getheader('content-length')
        nbytes = int(length)
        data = self.rfile.read(nbytes)
        self.end_headers()

        path = self.path
        print "[PATH] {0}".format(path)
        #设置response返回的josn内容
        if path == "/setJsonForResponse":
            print "[URI] /setJsonForResponse"
            response_data = json.loads(data)
            self.RESPONSE_CODE = response_data["response_code"]
            self.RESPONSE = response_data["response_result"]
            TestHTTPHandler.RESPONSE_CODE = self.setJsonForResponse(self.RESPONSE_CODE,self.RESPONSE,"")
            TestHTTPHandler.RESPONSE = self.RESPONSE

        #创建缓存云实例接口
        if path == "/action?op=create":
            print "[URI] /action?op=create"
            print ""
            self.generateJsonForResponse(self.RESPONSE_CODE,"default response for create instance")
        #删除缓存云实例接口
        if path == "/action?op=delete":
            print "[URI] /action?op=delete"
            print ""
            self.generateJsonForResponse(self.RESPONSE_CODE,"default response for delete instance")
        #扩容
        if path  == "/action?op=scale":
            print "[URI] /action?op=scale"
            print ""
            self.generateJsonForResponse(self.RESPONSE_CODE,"default response for scaler instance")
        #缩容
        if path  == "/action?op=merge":
            print "[URI] /action?op=merge"
            print ""
            self.generateJsonForResponse(self.RESPONSE_CODE,"default response for merge instance")

    def setJsonForResponse(self, response_code, response_result, message):
        print "[INFO] {0},{1}".format(self.RESPONSE_CODE, self.RESPONSE)
        self.RESPONSE = response_result
        if self.RESPONSE == None:
            if self.RESPONSE_CODE == 200:
                self.returnResponse(200,response_result, message)
            if self.RESPONSE_CODE == 500:
                self.returnResponse(500, "", "SERVER EXCEPTION")
            return

        self.returnResponse(self.RESPONSE_CODE,self.RESPONSE, message)
        print "[RESPONSE] {0}".format(self.RESPONSE)
        return response_code

    def returnResponse(self, response_code, response_data, message):
        print "[INFO] The code of http response is {0}".format(response_code)
        if response_code is None:
            print "[ERROR] The code of http response is null"
            return
        if response_code == 200:
            self.send_response(200, message)
            self.wfile.write(response_data)
        elif response_code == 500:
            self.send_response(500, "SERVER CAN NOT RESPONSE")
            self.wfile.write("")
        elif response_code == 404:
            self.send_response(404, "CAN NOT FIND TARGET PAGE")
            self.wfile.write("")
        else:
            self.send_response(response_code, message)
            self.wfile.write(response_data)

    #设置正确的HTTP请求的场景
    def generateJsonForResponse(self, response_code, message):
        print "[INFO] Data for request is {0}".format(self.RESPONSE)
        if self.RESPONSE == None:
            response_json = "{\"code\":0,\"msg\":\"success\",\"Data\":{\"" + message + "\"}"
            self.returnResponse(self.RESPONSE_CODE, response_json, "DEFAULT RESPONSE")
        else:
            self.returnResponse(self.RESPONSE_CODE, self.RESPONSE, "RESPONSE SETTED UP")

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('127.0.0.1', 8000), TestHTTPHandler)  #在本地8080端口上启用httpserver
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()