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
from core.speaker import Speaker
from commons import Utilities
from commons import EventLogger
from commons import ProcessParallel
import threading
import os

class Person(BaseModel):
	def __init__(self, group=None, name=None, alias=None):
		super(Person, self).__init__()
		self.group = group
		self.name = name
		self.id = ''
		self.activeRecords = PersonActiveRecords(self)
		self.cognitive = PersonCognitive(self)
		self.alias = alias

	def newFaceFromImage(self, image):
		return PersonFace(self, image)

	@staticmethod
	def register(group, alias):
		data_path = Utilities.absolutePathForFile(
			Utilities.defaultDataPath(),
			alias
		)

		with open(os.path.join(data_path, 'name.txt'), 'r') as file:
			name = file.read()
			person = group.newPersonWithName(name)
			person.alias = alias;
			create_voice_thread = threading.Thread(
				name="create_voice",
				target=Person.__create_voice,
				args=(name, alias)
			)
			person.save()

			save_faces_thread = threading.Thread(
				name="save_faces",
				target=Person.__save_faces,
				args=(person, data_path)
			)

			processes = ProcessParallel(create_voice_thread, save_faces_thread)
			processes.fork_threads()
			processes.start_all()
			processes.join_all()

	@staticmethod
	def __create_voice(name, alias):
		Speaker.create_voice(name, alias)

	@staticmethod
	def __save_faces(person, data_path):
		files = os.listdir(data_path)
		for file in files:
			if file != 'name.txt':
				personFace = person.newFaceFromImage(os.path.join(data_path, file))
				personFace.save()