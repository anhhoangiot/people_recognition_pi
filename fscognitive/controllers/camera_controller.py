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
		group = ModelFactory.registeredUsersGroup()
		group.save()
		person = group.newPersonWithName(name)
		person.save()
		faces = self.__record(True)
		for face in faces:
			personFace = person.newFaceFromImage(face)
			personFace.save()
		group.cognitive.train()

	def idetifyPerson(self):
		registeredUsersGroup = ModelFactory.registeredUsersGroup()
		faces = self.__record(False)
		registeredUsersGroup.identify(faces)		

	def __record(self, isRegister):
		print 'Start capturing...'
		recognizer = FaceRecognizer()
		recognizer.startFaceCapturing(isRegister)
		return recognizer.capturedFaces()
