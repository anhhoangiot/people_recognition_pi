#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

import sqlite3
import abc


class BaseActiveRecords(object):
    def __init__(self):
        super(BaseActiveRecords, self).__init__()

    def __openConnection(self):
        try:
            connection = sqlite3.connect('resources/db/speech.db')
            return connection
        except Exception as e:
            print "Connection error: {0}".format(e)
            return None

    @abc.abstractmethod
    def createTable(self):
        ''' Create table if not exist in sqlite '''
        return

    @abc.abstractmethod
    def save(self):
        ''' Save record into database '''
        return

    def execute(self, query):
        self.connection = self.__openConnection()
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            self.connection.close()

    def executeQuery(self, query):
        self.connection = self.__openConnection()
        if self.connection is not None:
            cursor = self.connection.cursor()
            result = cursor.execute(query)
            return result
