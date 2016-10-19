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

from activeRecords import PersonActiveRecords
from core.cognitive import PersonCognitive
from base_model import BaseModel
from person_face import PersonFace
from confidence import Confidence

class Person(BaseModel):
	def __init__(self, group, name):
		super(Person, self).__init__()
		self.group = group
		self.name = name
		self.id = ''
		self.activeRecords = PersonActiveRecords(self)
		self.cognitive = PersonCognitive(self)

	def newFaceFromImage(self, image):
		return PersonFace(self, image)


	def verify(self, faces):
		verifyResults = []	
		for face in faces:
			personFace = self.newFaceFromImage(face)
			personFace.cognitive.detect()
			result = personFace.cognitive.verify(self)
			if result != None:
				verifyResults.append(result)
		return self.__confidence(verifyResults)
		
	def __confidence(self, results):
		weight = 1.0
		finalConfidence = 0.0
		if len(results) > 0:
			for result in results:
				confidence = 0.0
				if result != None and result['isIdentical'] == True:
					confidence = weight * result['confidence']
				finalConfidence += confidence
			finalConfidence /= len(results)
		return finalConfidence