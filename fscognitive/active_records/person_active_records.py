#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from base_active_records import BaseActiveRecords


class PersonActiveRecords(BaseActiveRecords):
    def __init__(self, person):
        super(PersonActiveRecords, self).__init__()
        self.person = person

    def createTable(self):
        createTableQuery = '''
            CREATE TABLE IF NOT EXISTS person (
                personId text,
                groupId text,
                name text,
                alias text
            )
        '''
        self.execute(createTableQuery)

    def save(self):
        if self.person.id != '':
            self.__delete()
            self.__insert()
            print 'Saved person: %s' % self.person.name
            return True
        print 'Person id is missing'
        return False

    def find(self, id):
        getOwner = '''
            SELECT name, alias FROM person WHERE personId="%s"
        ''' % id
        people = self.executeQuery(getOwner)
        return people.fetchone()

    def __insert(self):
        insertPerson = '''
            INSERT INTO person VALUES ("%s", "%s", "%s", "%s")
        ''' % (
            str(self.person.id),
            self.person.group.id,
            self.person.name,
            self.person.alias)
        self.execute(insertPerson)

    def __delete(self):
        deletePerson = '''
            DELETE FROM person WHERE name="%s" AND groupId="%s"
        ''' % (self.person.name, self.person.group.id)
        self.execute(deletePerson)
