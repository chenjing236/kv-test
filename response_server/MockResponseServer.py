#!/usr/bin/env python
# encoding: utf-8
import BaseHTTPServer
import json

class TestHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    RESPONSE = None
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
            self.setJsonForResponse(data)
            RESPONSE = None
        #设置错误场景,curl -s -XPOST --data '{"response_code":501,"response":"can not find service"}' "http://127.0.0.1:8000/setResponseForError"
        if path == "/setResponseForError":
            print "[URI] /setResponseForError"
            json_data = json.loads(data)
            response_code = json_data["response_code"]
            response_result = json_data["response"]
            self.generateResponseForError(response_code, response_result)
        #创建缓存云实例接口
        if path == "/action?op=create":
            print "[URI] /action?op=create"
            print ""
            self.generateJsonForResponse("default response for create instance")
        #删除缓存云实例接口
        if path == "/action?op=delete":
            print "[URI] /action?op=delete"
            print ""
            self.generateJsonForResponse("default response for delete instance")
        #扩容
        if path  == "/action?op=scale":
            print "[URI] /action?op=scale"
            print ""
            self.generateJsonForResponse("default response for scaler instance")
        #缩容
        if path  == "/action?op=merge":
            print "[URI] /action?op=merge"
            print ""
            self.generateJsonForResponse("default response for merge instance")

    def setJsonForResponse(self,data):
        TestHTTPHandler.RESPONSE = data
        if data == "":
            self.send_response(50001, "Set up json for response")
            #self.wfile.write("\r\n Json for response is null.")
            self.wfile.write("Json for response is null.")
            return

        self.send_response(200, "Set up json for response")
        #self.wfile.write("\r\n")
        self.wfile.write(data)
        print "[RESPONSE] {0}".format(TestHTTPHandler.RESPONSE)

    #设置正确的HTTP请求的场景
    def generateJsonForResponse(self,message):
        if TestHTTPHandler.RESPONSE == None:
            self.send_response(200,"DEFAULT RESPONSE")
            #self.wfile.write("\r\n")
            response_json = "{\"code\":0,\"msg\":\"success\",\"Data\":{\"" + message + "\"}"
            self.wfile.write(response_json)
        else:
            self.send_response(200,"RESPONSE SETTED UP")
            #self.wfile.write("\r\n")
            self.wfile.write(TestHTTPHandler.RESPONSE)

    #设置错误的HTTP返回场景
    def generateResponseForError(self,response_code,response_result):
        if response_code is None or response_result is None:
            print "[ERROR] Please set up response code and response result"
            return
        if response_code == 500:
            self.send_response(500,"RESPONSE OF SERVER IS INCORRECT")
            self.wfile.write(None)
        if response_code == 404:
            self.send_response(404,"CAN NOT FIND SERVICE")
            self.wfile.write(None)
        if response_code == 403:
            self.send_response(403,"CAN NOT REDIRECT TO TARGET PAGE")
            self.wfile.write(None)
        if response_code is not 500 and response_code is not 404 and response_code is not 403:
            self.send_response(response_code, response_result)
            self.wfile.write(None)

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('127.0.0.1', 8000), TestHTTPHandler)  #在本地8080端口上启用httpserver
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()