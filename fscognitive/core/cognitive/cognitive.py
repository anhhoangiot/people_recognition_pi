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

import cognitive_face
import abc
import json
from commons import Utilities

class Cognitive(object):
	def __init__(self):
		super(Cognitive, self).__init__()
		self.api = cognitive_face
		with open(Utilities.absolutePathForFile(__file__,'secret.json')) as data_file:
			data = json.load(data_file)
			KEY = data['secret']
			self.api.Key.set(KEY)

	@abc.abstractmethod
	def processResponse(self, response, callback=None):
		''' Process json message return by service '''
		return

	@abc.abstractmethod
	def save(self):
		''' Make a request to create a record in MS cognitive service '''
		return

	def stringify(self, response):
		return json.dumps(response)

	def dictionarize(self, response):
		return json.loads(self.stringify(response))

	def printResponse(self, response):
		print response