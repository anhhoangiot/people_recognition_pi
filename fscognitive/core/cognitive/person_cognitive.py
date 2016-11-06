#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from cognitive import Cognitive
from commons import EventLogger

logger = EventLogger.logger()


class PersonCognitive(Cognitive):
    def __init__(self, person):
        super(PersonCognitive, self).__init__()
        self.person = person

    def save(self):
        if self.isExisted() is False:
            try:
                result = self.api.person.create(
                    self.person.group.id, self.person.name)
                self.processResponse(result, None)
                return True
            except self.api.CognitiveFaceException as e:
                logger.log(e)
                return False
        return True

    def isExisted(self):
        if self.person.id:
            try:
                self.api.person.get(self.person.group.id, self.person.id)
                return True
            except self.api.CognitiveFaceException as e:
                logger.log(e)
                return False
        return False

    def processResponse(self, response, callback=None):
        response = self.dictionarize(response)
        self.person.id = response['personId']
        if callback:
            callback(response)
