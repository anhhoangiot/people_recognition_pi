#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from active_records import PersonFacesActiveRecords
from active_records import PersonGroupActiveRecords
from active_records import PersonActiveRecords


class Configurator(object):
    @staticmethod
    def config_application():
        print 'Setting up database...'
        PersonGroupActiveRecords(None).createTable()
        PersonActiveRecords(None).createTable()
        PersonFacesActiveRecords(None).createTable()
        print 'Finished setting database!'
