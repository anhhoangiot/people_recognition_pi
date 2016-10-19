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

from models import ModelFactory
from models import Confidence
from core.face_recognizer import FaceRecognizer

class CameraController(object):
	def __init__(self):
		super(CameraController, self).__init__()

	def registerPerson(self):
		name = raw_input('Name:')
		self.__registerPersonWithName(name)

	def __registerPersonWithName(self, name):
		group = ModelFactory.ownerGroup()
		group.save()
		person = group.newPersonWithName(name)
		person.save()
		faces = self.__record()
		for face in faces:
			personFace = person.newFaceFromImage(face)
			personFace.save()

	def verifyPerson(self):
		ownerGroup = ModelFactory.ownerGroup()
		owners = ownerGroup.owners()
		faces = self.__record()
		isOwner = False
		considerList = []
		for person in owners:
			confidence = person.verify(faces)
			confidenceLevel = Confidence.confidenceLevel(confidence)
			if confidenceLevel == Confidence.High:
				isOwner = True
				break
			elif confidenceLevel == Confidence.Medium:
				considerList.append({'person': person, 'confidence': confidence})
			
		if isOwner:
			return self.__highConfidence(person)
		elif len(considerList) > 0:
			return self.__mediumConfidence(considerList)
		else:
			return self.__lowConfidence()

	def __highConfidence(self, person):
		print 'Hello, %s' % person.name
		return True

	def __mediumConfidence(self, considerList):
		highestCofidence = 0.0
		highestCofidencePerson = None
		for dictionary in considerList:
			if dictionary['confidence'] > highestCofidence:
				highestCofidence = dictionary['confidence']
				highestCofidencePerson = dictionary['person']
		print 'Sorry, I might be wrong. Are you %s?' % highestCofidencePerson.name
		return False

	def __lowConfidence(self):
		print 'Sorry, I don\'t recognize you.'
		# Will be person real name 
		name = raw_input('Name:')
		self.__registerPersonWithName(name)
		return False

	def __record(self):
		print 'Start capturing...'
		recognizer = FaceRecognizer()
		recognizer.startFaceCapturing()
		return recognizer.capturedFaces()
