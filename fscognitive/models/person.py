#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from active_records import PersonActiveRecords
from core.cognitive import PersonCognitive
from base_model import BaseModel
from person_face import PersonFace
from core.speaker import Speaker
from commons import Utilities
from commons import ProcessParallel
import threading
import os


class Person(BaseModel):
    def __init__(self, group=None, name=None, alias=None):
        super(Person, self).__init__()
        self.group = group
        self.name = name
        self.id = ''
        self.active_records = PersonActiveRecords(self)
        self.cognitive = PersonCognitive(self)
        self.alias = alias

    def face_from_image(self, image):
        return PersonFace(self, image)

    @staticmethod
    def register(group, alias):
        data_path = Utilities.absolute_path(
            Utilities.train_data_path(),
            alias
        )

        with open(os.path.join(data_path, 'name.txt'), 'r') as file:
            name = file.read()
            person = group.person_with_name(name)
            person.alias = alias
            create_voice_thread = threading.Thread(
                name="create_voice",
                target=Person.__create_voice,
                args=(name, alias)
            )
            person.save()

            save_faces_thread = threading.Thread(
                name="save_faces",
                target=Person.__save_faces,
                args=(person, data_path)
            )

            processes = ProcessParallel(create_voice_thread, save_faces_thread)
            processes.fork_threads()
            processes.start_all()
            # Wait until all threads are done
            processes.join_all()

    @staticmethod
    def __create_voice(name, alias):
        Speaker.create_voice(name, alias)

    @staticmethod
    def __save_faces(person, data_path):
        files = os.listdir(data_path)
        for file in files:
            if file != 'name.txt' and file != 'region.txt':
                personFace = person.face_from_image(
                    os.path.join(data_path, file))
                personFace.save()
