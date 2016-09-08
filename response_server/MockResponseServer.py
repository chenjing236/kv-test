#!/usr/bin/env python
# encoding: utf-8
import BaseHTTPServer

class TestHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    RESPONSE = ""
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if self.path == "/getCluster":
            self.send_response(200)
            data="\r\n{\"code\":0,\"message\":\"get cluster\"}"
        else:
            self.send_response(404,"Incorrect request uri")
            data = "\r\n{\"code\":1,\"message\":\"URI is incorrect\"}"

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
        #创建缓存云实例接口
        if path == "/action?op=create":
            print "[URI] /action?op=create"
            self.generateJsonForResponse("default response for create instance")
        #删除缓存云实例接口
        if path == "/action?op=delete":
            print "[URI] /action?op=delete"
            self.generateJsonForResponse("default response for delete instance")
        #扩容
        if path  == "/action?op=scale":
            print "[URI] /action?op=scale"
            self.generateJsonForResponse("default response for scaler instance")
        #缩容
        if path  == "/action?op=merge":
            print "[URI] /action?op=merge"
            self.generateJsonForResponse("default response for merge instance")

    def setJsonForResponse(self,data):
        TestHTTPHandler.RESPONSE = data
        if data == "":
            self.send_response(50001, "Set up json for response")
            self.wfile.write("\r\n Json for response is null.")
            return

        self.send_response(200, "Set up json for response")
        self.wfile.write("\r\n")
        self.wfile.write(data)
        print "[RESPONSE] {0}".format(TestHTTPHandler.RESPONSE)

    def generateJsonForResponse(self,message):
        if TestHTTPHandler.RESPONSE == "":
            self.send_response(200,"DEFAULT RESPONSE")
            self.wfile.write("\r\n")
            response_json = "{\"code\":0,\"msg\":\"success\",\"Data\":{\"" + message + "\"}"
            self.wfile.write(response_json)
        else:
            self.send_response(200,"RESPONSE SETTED UP")
            self.wfile.write("\r\n")
            self.wfile.write(TestHTTPHandler.RESPONSE)

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('127.0.0.1', 8000), TestHTTPHandler)  #在本地8080端口上启用httpserver
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()