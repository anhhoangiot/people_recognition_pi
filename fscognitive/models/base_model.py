#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0


class BaseModel(object):
    def __init__(self):
        super(BaseModel, self).__init__()
        self.cognitive = None
        self.active_records = None

    def save(self):
        if self.cognitive is not None and self.active_records is not None:
            if self.cognitive.save():
                self.active_records.save()
