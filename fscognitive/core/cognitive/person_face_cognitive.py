#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from cognitive import Cognitive
from commons import EventLogger

logger = EventLogger.logger()


class PersonFaceCognitive(Cognitive):

    def __init__(self, face):
        super(PersonFaceCognitive, self).__init__()
        self.face = face

    def save(self):
        if self.isExisted() is False:
            try:
                result = self.api.person.add_face(
                    self.face.image,
                    self.face.person.group.id,
                    self.face.person.id
                )
                self.processResponse(result, self.__savePersistedFace)
                return True
            except self.api.CognitiveFaceException as exception:
                logger.log(exception)
                return False
        return True

    def isExisted(self):
        if self.face.id:
            try:
                self.api.face.get_face(
                    self.face.person.group.id,
                    self.face.person.id,
                    self.face.id
                )
                return True
            except self.api.CognitiveFaceException as exception:
                logger.log(exception)
                return False
        return False

    def detect(self):
        try:
            result = self.api.face.detect(self.face.image)
            self.processResponse(result, self.__saveNonPersistedFace)
            return True
        except self.api.CognitiveFaceException as exception:
            logger.log(exception)
            return False

    def verify(self, person):
        try:
            result = self.api.face.verify(
                self.face.id,
                None,
                person.group.id,
                person.id,
            )
            return self.dictionarize(result)
        except self.api.CognitiveFaceException as exception:
            logger.log(exception)

    def __savePersistedFace(self, response):
        self.face.id = response['persistedFaceId']

    def __saveNonPersistedFace(self, response):
        self.face.id = response[0]['faceId']

    def processResponse(self, response, callback=None):
        response = self.dictionarize(response)
        if callback:
            callback(response)
