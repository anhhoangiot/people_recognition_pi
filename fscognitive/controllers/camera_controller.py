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
from models import Person
from core.face_recognizer import FaceRecognizer
from commons import EventLogger
from commons import Utilities
import os
import time

logger = EventLogger.logger()

class CameraController(object):
	"""Control camera device to register or identify people"""
	def __init__(self):
		super(CameraController, self).__init__()

	def register(self, data_path):
		"""Register a group of people specified in data folder and train

			Args:
				data_path (string): train data folder
		"""
		if data_path == 'default':
			data_path = Utilities.train_data_path()
		if Utilities.file_exists(data_path):
			group = ModelFactory.registered_group()
			group.save()
			for alias_name in os.listdir(data_path):
				# Ignore gitkeep file and collect data from all folders
				if alias_name != '.gitkeep':
					logger.log('Registering %s...' %alias_name)
					Person.register(group, alias_name)
			# After everything is done, call api to train newly created group
			self.train()

	def identify(self):
		"""Identify a person or a group of people captured by camera"""
		registered_group = ModelFactory.registered_group()
		faces = self.record(False)
		registered_group.identify(faces)
	# 
	# Functions for internal uses
	#

	def train(self):
		"""Enqueue an event to train person group and report train progress"""
		group = ModelFactory.registered_group()
		group.cognitive.train()
		# Keep querying training status every 1 second
		while True:
			train_result = group.cognitive.trainingStatus()
			# Completed training event will have status succeeded or failed
			if train_result['status'] == 'succeeded' or 
			   train_result['status'] == 'failed':
				break
			time.sleep(1)		

	def record(self, is_register):
		"""Start the camera and capture faces
			
			Args:
				is_register (bool): determine if the session is registering or identifying
					If this argument is true then camera will capture 3 photos of user.
					Otherwise, only 1 photo is captured

			Returns:
				Array: an array of captured images

		"""
		logger.log('Start capturing...')
		# Remember that one computer can have multiple cameras
		# The first camera will have index 0 and so on
		recognizer = FaceRecognizer(1)
		recognizer.start_capturing(is_register)
		return recognizer.captured_faces()
