#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from commons import Utilities
import cv2
import time
import glob
import os

DEFAULT_FACES = 4


class FaceRecognizer:
    """This class recognizes faces in camera and captures them"""

    def __init__(self, camera):
        """Initialization

                Args:
                        camera (int): index of camera to use
        """
        self.cascade_file = Utilities.absolute_path(__file__, 'cascade.xml')
        self.face_cascade = cv2.CascadeClassifier(self.cascade_file)
        self.video_capture = cv2.VideoCapture(camera)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        self.faces_captured = 1

    def start_capturing(self, is_register):
        """Start the camera, look for faces and write to file when faces are captured

                Args:
                        is_register (bool): determine if the session is
                        registering or identifying
                            If this argument is true then camera will capture 3
                            photos of user. Otherwise, only 1 photo is captured
        """
        if is_register is False:
            self.faces_captured = DEFAULT_FACES - 1
        while self.faces_captured < DEFAULT_FACES:
            # Read frame from video capture
            return_code, frame = self.video_capture.read()
            # Use Haar cascade to detect faces in captured frame
            faces = self.face_cascade.detectMultiScale(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            # Looping through captured faces and write to file
            for (x, y, w, h) in faces:
                # All captured images will be saved in tmp folder in
                # core/face_recognizer
                filePath = Utilities.absolute_path(
                    __file__, 'tmp/face%d.jpg' % self.faces_captured)
                self.faces_captured += 1
                cv2.imwrite(filePath, frame)
                if is_register:
                    # Sleep 2 seconds so user can change face orientation
                    time.sleep(2)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_capturing()
                break

            # cv2.imshow('Video', frame)

        self.stop_capturing()

    def stop_capturing(self):
        """End camera session"""
        self.video_capture.release()
        cv2.destroyAllWindows()

    def captured_faces(self):
        """Get all captured images"""
        dir = os.path.dirname(__file__)
        return glob.glob(os.path.join(dir, 'tmp') + "/*.jpg")
