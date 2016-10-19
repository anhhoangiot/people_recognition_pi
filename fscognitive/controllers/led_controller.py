#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

'''
Copyright (c) 2016 Anh Hoang

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import socket
import sys
from thread import *
import urllib2
import json

class LEDController(object):
    HOST = ''
    PORT = 8888 
    def __init__(self):
        super(LEDController, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created!'

    def start(self):
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as message:
            print 'Bind failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
        print 'Socket bind complete!'
        self.socket.listen(10)
        print 'Socket now listening!'
        while True:
            connection, address = self.socket.accept()
            print 'Connected with ' + address[0] + ':' + str(address[1])
            start_new_thread(receiveCommandThread, (connection,))
        self.socket.close()

    def __receiveCommandThread(self, connection):
        connection.send('authorized')
        while True:
            try:
                command = connection.recv(1024)
                if not command:
                    break;
                print 'Received command: ' + command
                self.__processReceivedCommand(command);
            except Exception, e:
                print 'Connection error'
                break;

        connection.close()

    def __processReceivedCommand(self, command):
        if command:
            status = 'off'
            if command == '1':
                print 'Turning light on'
                status = 'on'
            else:
                print 'Turning light off'
                status = 'off'
            self.__sendLedStatusToCloud(status)

    def __sendLedStatusToCloud(self, status):
        print 'Sending led status ' + status
        data = {
            'status': status,
            'name': 'LED 1'
        }
        request = urllib2.Request('http://pociot.azurewebsites.net/')
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request, json.dumps(data))