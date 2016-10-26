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
from commons import Utilities
from commons import EventLogger
import os
import time

logger = EventLogger.logger()

class CameraController(object):
	def __init__(self):
		super(CameraController, self).__init__()

	def registerGroup(self, data_path):
		if data_path == 'default':
			data_path = Utilities.defaultDataPath()
		if Utilities.fileExistsAtPath(data_path):
			for folder in os.listdir(data_path):
				group = ModelFactory.registeredUsersGroup()
				group.save()
				self.__registerPersonWithDataAtPath(folder)

	def __registerPersonWithDataAtPath(self, folder):
		data_path = Utilities.absolutePathForFile(
			Utilities.defaultDataPath(),
			folder
		)

		with open(os.path.join(data_path, 'name.txt'), 'r') as file:
			name = file.read()
			group = ModelFactory.registeredUsersGroup()
			person = group.newPersonWithName(name)
			person.save()

		files = os.listdir(data_path)

		for file in files:
			if file != 'name.txt':
				personFace = person.newFaceFromImage(os.path.join(data_path, file))
				personFace.save()

		group.cognitive.train()

		while True:
			train_result = group.cognitive.trainingStatus()
			if train_result['status'] == 'succeeded':
				break
			time.sleep(1)

	def idetifyPerson(self):
		registeredUsersGroup = ModelFactory.registeredUsersGroup()
		faces = self.__record(False)
		registeredUsersGroup.identify(faces)		

	def __record(self, isRegister):
		logger.log('Start capturing...')
		recognizer = FaceRecognizer()
		recognizer.startFaceCapturing(isRegister)
		return recognizer.capturedFaces()
