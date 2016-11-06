#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from base_active_records import BaseActiveRecords


class PersonFacesActiveRecords(BaseActiveRecords):
    def __init__(self, face):
        super(PersonFacesActiveRecords, self).__init__()
        self.face = face

    def createTable(self):
        createTableQuery = '''
            CREATE TABLE IF NOT EXISTS personFaces (
                personId text,
                faceId text
            )
        '''
        self.execute(createTableQuery)

    def save(self):
        if self.face.id != '':
            self.__delete()
            self.__insert()
            print 'Saved face of person: %s' % self.face.person.name
            return True
        print 'Face id is missing'
        return False

    def __insert(self):
        insertFace = '''
            INSERT INTO personFaces VALUES ("%s", "%s")
        ''' % (str(self.face.person.id), str(self.face.id))
        self.execute(insertFace)

    def __delete(self):
        deleteFace = '''
            DELETE FROM personFaces WHERE personId="%s" AND faceId="%s"
        ''' % (str(self.face.person.id), str(self.face.id))
        self.execute(deleteFace)
