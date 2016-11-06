#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

import cognitive_face
import abc
import json
from commons import Utilities


class Cognitive(object):
    def __init__(self):
        super(Cognitive, self).__init__()
        self.api = cognitive_face
        file_path = Utilities.absolute_path(__file__, 'secret.json')
        with open(file_path) as data_file:
            data = json.load(data_file)
            KEY = data['secret']
            self.api.Key.set(KEY)

    @abc.abstractmethod
    def processResponse(self, response, callback=None):
        """Process json message return by service"""
        return

    @abc.abstractmethod
    def save(self):
        """Make a request to create a record in MS cognitive service"""
        return

    def stringify(self, response):
        return json.dumps(response)

    def dictionarize(self, response):
        return json.loads(self.stringify(response))

    def print_response(self, response):
        print response
