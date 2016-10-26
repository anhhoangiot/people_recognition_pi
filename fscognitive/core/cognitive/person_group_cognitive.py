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
from person_cognitive import PersonCognitive
from commons import EventLogger

logger = EventLogger.logger()

class PersonGroupCognitive(Cognitive):
	"""Intermidiate module works as an interface between group model and MS service

		Attributes:
			group (PersonGroup): group object which initialize instance of this class

	"""

	def __init__(self, group):
		super(PersonGroupCognitive, self).__init__()
		self.group = group

	def identify(self, faces):
		"""Identify a group of people from captured faces
			
			Args:
				faces (Array): list of captured faces id returned from MS service

			Returns:
				Array: list of people identified from faces

		"""
		logger.log('Identifying...')
		candidates = []
		try:
			response = self.api.face.identify(faces, self.group.id)
			people = self.dictionarize(response)
			candidates = []
			for person in people:
				candidate = person['candidates'][0]['personId']
				candidates.append(candidate)
		except self.api.CognitiveFaceException as exception:
			logger.log(exception)
		finally:
			return candidates

	def save(self):
		"""Save a new person group in MS service"""
		logger.log('Saving person group...')
		# Only create group if it does not exist
		if self.isExisted() == False:
			try:
				self.api.person_group.create(self.group.id, self.group.name)
				logger.log(
					'Created person group with name %s' % self.group.name
				)
				return True
			except self.api.CognitiveFaceException as exception:
				logger.log(exception)
				return False
		return True

	def isExisted(self):
		"""Check if group is existed or not"""
		try:
			self.api.person_group.get(self.group.id)
			return True
		except self.api.CognitiveFaceException as exception:
			logger.log(exception)
			return False

	def train(self):
		"""Enqueue a group to be trained"""
		logger.log('Enqueue group training task...')
		result = self.api.person_group.train(self.group.id)
		self.processResponse(result, self.printResponse)

	def trainingStatus(self):
		"""Get training status"""
		logger.log('Fetching training status...')
		result = self.api.person_group.get_status(self.group.id)
		return self.processResponse(result, self.printResponse)

	def processResponse(self, response, callback=None):
		response = self.dictionarize(response)
		if callback:
			callback(response)
		return response
