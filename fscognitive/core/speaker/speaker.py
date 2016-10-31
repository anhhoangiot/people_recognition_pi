#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-10
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

import requests
import json
import wget
import pygame
import os
import time
from commons import Utilities

class Speaker():
	def __init__(self):
		super(Speaker, self).__init__()

	@staticmethod
	def speak(alias):
		sounds_dir = Utilities.names_dir()
		save_dir = Utilities.absolutePathForFile(sounds_dir, alias + '.mp3')
		if os.path.exists(save_dir) == True:
			# print save_dir
			pygame.mixer.init(44100, -16, 2, 2048)
			pygame.mixer.music.load(save_dir)
			pygame.mixer.music.play()
			time.sleep(1.05)

	@staticmethod
	def create_voice(text, alias):
		sounds_dir = Utilities.names_dir()
		save_dir = Utilities.absolutePathForFile(sounds_dir, alias + '.mp3')
		if os.path.exists(save_dir) == False:
			headers = {
				'Content-Type': 'application/json',
				'api_key': 'b5db987b5a944ff78097d435a5a564dc'
			}
			try:
				response = requests.request(
					'POST',
					'http://api.openfpt.vn/text2speech/v3',
					headers=headers,
					data=text
				)
				if response.status_code not in (200, 202):
					print response.status_code
				if response.text:
					result = response.json()
					if result['async']:
						wget.download(result['async'], save_dir)
			except Exception as e:
				print e