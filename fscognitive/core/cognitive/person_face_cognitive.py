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

from cognitive import Cognitive

class PersonFaceCognitive(Cognitive):
	def __init__(self, face):
		super(PersonFaceCognitive, self).__init__()
		self.face = face

	def save(self):
		if self.isExisted() == False:
			try:
				result = self.api.person.add_face(
					self.face.image, 
					self.face.person.group.id, 
					self.face.person.id
				)
				self.processResponse(result, self.__savePersistedFace)
				return True
			except self.api.CognitiveFaceException as e:
				return False
		return True

	def isExisted(self):
		if self.face.id:
			try:
				result = self.api.face.get_face(
					self.face.person.group.id, 
					self.face.person.id,
					self.face.id
				)
				return True
			except self.api.CognitiveFaceException as e:
				return False
		return False

	def detect(self):
		try:
			result = self.api.face.detect(self.face.image)
			self.processResponse(result, self.__saveNonPersistedFace)
			return True
		except Exception as e:
			print e
			return False

	def verify(self, person):
		try:
			result = self.api.face.verify(
				self.face.id, 
				None,
				person.group.id,
				person.id, 
			)
			# print result
			return self.dictionarize(result)
		except Exception as e:
			print e

	def __savePersistedFace(self, response):
		self.face.id = response['persistedFaceId']

	def __saveNonPersistedFace(self, response):
		self.face.id = response[0]['faceId']

	def processResponse(self, response, callback=None):
		response = self.dictionarize(response)
		if callback:
			callback(response)
