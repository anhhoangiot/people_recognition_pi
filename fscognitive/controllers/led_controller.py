#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

import socket
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
            print 'Bind failed. Error Code : ' + str(message[0])
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
                    break
                print 'Received command: ' + command
                self.__processReceivedCommand(command)
            except Exception, e:
                print 'Connection error: %s' % e
                break

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
        print response
