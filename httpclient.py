#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, url):
        # use sockets!
        parse = urlparse(url)

        try:
            host, port = parse.netloc.split(':')
        except ValueError:
            host, port = parse.netloc, 80
        
        sockets = socket.create_connection((host, port), 15)
        return sockets


    def get_code(self, data):
        code = data.split()[1]
        return int(code)

    def get_headers(self,data,type,arg):

        if (type=="GET"):
            header = "GET " + data + " HTTP/1.0\n\n"
            return header

        elif(type=="POST"):
            header = "POST " + data + " HTTP/1.0\n"
            if arg != None:
                postdata = urllib.urlencode(arg)
                header += ('Content-Length: '+
                             str(len(postdata))+'\n\n'+
                             postdata)
            
            return header + "\n"
        
        return None

    def get_body(self, data):
        counter = 0
        lines = data.splitlines()
        counter = lines.index("")
        return "\r\n".join(lines[counter:])

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        soc = self.connect(url)
        Header = self.get_headers(url,"GET",args)
        soc.sendall(Header)
        return_value = self.recvall(soc)
        code = self.get_code(return_value)
        body = self.get_body(return_value)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        soc = self.connect(url)
        Header = self.get_headers(url,"POST",args)
        soc.sendall(Header)
        return_value = self.recvall(soc)
        code = self.get_code(return_value)
        body = self.get_body(return_value)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
