#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from person_group import PersonGroup


class ModelFactory(object):
    @staticmethod
    def registered_group():
        return PersonGroup('face_recognizer_robot_raspberry_pi', 'owner')

        @staticmethod
        def guess_group():
            return PersonGroup('guess_group', 'guess')

    @staticmethod
    def person():
        return ModelFactory.registered_group().person_name('dummy')
