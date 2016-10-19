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
				name text
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

	def __insert(self):
		insertPerson = '''
			INSERT INTO person VALUES ("%s", "%s", "%s")
		''' % (str(self.person.id), self.person.group.id, self.person.name)
		self.execute(insertPerson)

	def __delete(self):
		deletePerson = '''
			DELETE FROM person WHERE name="%s" AND groupId="%s"
		''' % (self.person.name, self.person.group.id)
		self.execute(deletePerson)