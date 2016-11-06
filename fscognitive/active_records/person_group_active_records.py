#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from base_active_records import BaseActiveRecords


class PersonGroupActiveRecords(BaseActiveRecords):
    def __init__(self, group):
        super(PersonGroupActiveRecords, self).__init__()
        self.group = group

    def createTable(self):
        createTableQuery = '''
            CREATE TABLE IF NOT EXISTS personGroup (
                groupId text,
                groupName text
            )
        '''
        self.execute(createTableQuery)

    def save(self):
        if self.group.id:
            self.__delete()
            self.__insert()
            print 'Saved person group: %s' % self.group.name
            return True
        print 'Group id is missing'
        return False

    def containsPerson(self):
        getPerson = '''
            SELECT * FROM person WHERE groupId="%s"
        ''' % self.group.id
        people = self.executeQuery(getPerson)
        rows = len(people.fetchall())
        self.connection.close()
        return rows > 0

    def owners(self):
        getOwner = '''
            SELECT * FROM person WHERE groupId="%s"
        ''' % self.group.id
        people = self.executeQuery(getOwner)
        return people.fetchall()

    def __insert(self):
        insertPersonGroup = '''
            INSERT INTO personGroup VALUES ("%s", "%s")
        ''' % (self.group.id, self.group.name)
        self.execute(insertPersonGroup)

    def __delete(self):
        deletePersonGroup = '''
            DELETE FROM personGroup WHERE groupId="%s"
        ''' % self.group.id
        self.execute(deletePersonGroup)
