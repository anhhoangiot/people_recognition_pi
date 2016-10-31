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

import os
import sys

class Utilities:
	@staticmethod
	def file_exists(filePath):
		dir = os.path.dirname(__file__)
		absolutePath = os.path.join(dir, filePath)
		if os.path.exists(absolutePath) == False:
			print 'File not exist at path %s' % filePath
		return os.path.exists(absolutePath)

	@staticmethod
	def delete_file(filePath):
		dir = os.path.dirname(__file__)
		absolutePath = os.path.join(dir, filePath)
		if os.path.exists(absolutePath) == True:
			os.remove(absolutePath)
			print 'Deleted file at path %s' % filePath
		return os.path.exists(absolutePath)

	@staticmethod
	def absolute_path(directory, fileName):
		if os.path.isdir(directory):
			return os.path.join(directory, fileName)
		else:
			dir = os.path.dirname(directory)
			return os.path.join(dir, fileName)

	@staticmethod
	def project_directory():
		return os.path.dirname(__file__).strip('commons/')

	@staticmethod
	def train_data_path():
		return os.path.join(Utilities.project_directory(), 'resources\\datasets\\')

	@staticmethod
	def alias_path(alias):
		return os.path.join(Utilities.train_data_path(), alias)

	@staticmethod
	def voices_path():
		return os.path.join(Utilities.project_directory(), 'resources\\sounds\\names\\')