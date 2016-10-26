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

from commons import Configurator
from models import ModelFactory
from controllers import CameraController
from commons import EventLogger
import threading
import time
import argparse

def setup(condition):
	Configurator.configApplication()
	with condition:
		condition.notifyAll()

def start(condition, data_path=None, interval=0, verbose=True):
	with condition:
		group = ModelFactory.registeredUsersGroup()
		camera = CameraController()
		if data_path:
			condition.wait()
			camera.registerGroup(data_path)
		if interval > 0:
			while True:
				camera.idetifyPerson()
				time.sleep(interval)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--data_path')
	parser.add_argument('-i', '--interval', type=float)
	parser.add_argument('-v', '--verbose', action='store_true')

	args = parser.parse_args()
	condition = threading.Condition()
	verbose = True

	if args.verbose is None:
		verbose = False

	EventLogger.logger(verbose)

	if args.data_path:
		setUpThread = threading.Thread(
			name="setup", 
			target=setup, 
			args=(condition,)
		)
		mainThread = threading.Thread(
			name="main", 
			target=start, 
			args=(condition, args.data_path, 0, verbose,)
		)
		setUpThread.start()
		mainThread.start()

	if args.interval:
		mainThread = threading.Thread(
			name="main", 
			target=start, 
			args=(condition, None, args.interval, verbose,)
		)
		mainThread.start()