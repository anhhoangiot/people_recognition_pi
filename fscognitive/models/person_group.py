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

from activeRecords import PersonGroupActiveRecords
from core.cognitive import PersonGroupCognitive
from base_model import BaseModel
from person import Person
from person_face import PersonFace

class PersonGroup(BaseModel):
	def __init__(self, id, name):
		super(PersonGroup, self).__init__()
		self.id = id
		self.name = name
		self.activeRecords = PersonGroupActiveRecords(self)
		self.cognitive = PersonGroupCognitive(self)

	def newPersonWithName(self, name):
		return Person(self, name)

	def identify(self, faces):
		listFaces = []
		personFace = PersonFace()
		response = personFace.cognitive.api.face.detect(faces[0])
		detectedFaces = personFace.cognitive.dictionarize(response)
		for face in detectedFaces:
			listFaces.append(face["faceId"])
		recognizedPeople = self.cognitive.identify(listFaces)
		dummyPerson = self.newPersonWithName('dummy')
		peopleToSayHello = []
		for person in recognizedPeople:
			peopleToSayHello.append(dummyPerson.activeRecords.find(person)[0])
		for person in peopleToSayHello:
			print 'Xin chao %s' % person
