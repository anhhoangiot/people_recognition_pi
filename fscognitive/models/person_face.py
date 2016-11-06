#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from active_records import PersonFacesActiveRecords
from core.cognitive import PersonFaceCognitive
from base_model import BaseModel


class PersonFace(BaseModel):
    def __init__(self, person=None, image=None):
        super(PersonFace, self).__init__()
        self.person = person
        self.image = image
        self.id = ''
        self.active_records = PersonFacesActiveRecords(self)
        self.cognitive = PersonFaceCognitive(self)
