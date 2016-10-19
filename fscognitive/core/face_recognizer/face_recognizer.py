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

from commons import Utilities
import cv2
import sys
import time

class FaceRecognizer:
	def __init__(self):
		self.cascadeFilePath = Utilities.absolutePathForFile(__file__, 'cascade.xml')
		self.faceCascade = cv2.CascadeClassifier(self.cascadeFilePath)
		self.videoCapturer = cv2.VideoCapture(1)
		self.videoCapturer.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
		self.videoCapturer.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
		self.facesCaptured = 1

	def startFaceCapturing(self):
		while self.facesCaptured < 4:
			returnCode, frame = self.videoCapturer.read()

			faces = self.faceCascade.detectMultiScale(
				cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
				scaleFactor = 1.1,
				minNeighbors = 5,
				minSize = (30,30),
				flags = cv2.cv.CV_HAAR_SCALE_IMAGE
			)

			for (x, y, w, h) in faces:
				x = x - 40
				h = h + 80
				y = y - 40
				w = w + 80
				face = frame[y : y + h , x : x + w]
				cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 2)
				filePath = Utilities.absolutePathForFile(__file__, 'tmp/face%d.jpg' % self.facesCaptured)
				self.facesCaptured += 1
				cv2.imwrite(filePath, face)
				time.sleep(1)
				break

			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.stopFaceCapturing()
				break

			cv2.imshow('Video', frame)

		self.stopFaceCapturing()

	def stopFaceCapturing(self):
		self.videoCapturer.release()
		cv2.destroyAllWindows()

	def capturedFaces(self):
		faces = []
		for index in range(1,4):
			filePath = Utilities.absolutePathForFile(__file__, 'tmp/face%d.jpg' % index)
			faces.append(filePath)
		return faces

	def __enlargeImage(self, image):
		# First make it 16 times larger
		image = cv2.resize(image, (0,0), fx=4, fy=4)
		return image
