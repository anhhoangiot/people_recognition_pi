#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from active_records import PersonGroupActiveRecords
from core.cognitive import PersonGroupCognitive
from base_model import BaseModel
from person import Person
from person_face import PersonFace


class PersonGroup(BaseModel):
    def __init__(self, id, name):
        super(PersonGroup, self).__init__()
        self.id = id
        self.name = name
        self.active_records = PersonGroupActiveRecords(self)
        self.cognitive = PersonGroupCognitive(self)

    def person_with_name(self, name):
        return Person(self, name)

    def identify(self, faces):
        listFaces = []
        personFace = PersonFace()
        response = personFace.cognitive.api.face.detect(faces[0])
        detectedFaces = personFace.cognitive.dictionarize(response)
        for face in detectedFaces:
            listFaces.append(face["faceId"])
        recognizedPeople = self.cognitive.identify(listFaces)
        dummyPerson = self.person_with_name('dummy')
        peopleToSayHello = []
        for person_id in recognizedPeople:
            peopleToSayHello.append(
                dummyPerson.active_records.find(person_id)[1])
        return peopleToSayHello
