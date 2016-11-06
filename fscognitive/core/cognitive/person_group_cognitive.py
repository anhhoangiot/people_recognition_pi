#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from cognitive import Cognitive
from commons import EventLogger

logger = EventLogger.logger()


class PersonGroupCognitive(Cognitive):
    """Intermidiate module works as an interface between group model and MS service

            Attributes:
                    group (PersonGroup): group object which
                    initialized instance of this class

    """

    def __init__(self, group):
        super(PersonGroupCognitive, self).__init__()
        self.group = group

    def identify(self, faces):
        """Identify a group of people from captured faces

                Args:
                        faces (Array): list of captured faces id
                        returned from MS service

                Returns:
                        Array: list of people identified from faces

        """
        logger.log('Identifying...')
        candidates = []
        try:
            response = self.api.face.identify(faces, self.group.id)
            people = self.dictionarize(response)
            candidates = []
            for person in people:
                candidate = person['candidates'][0]['personId']
                candidates.append(candidate)
        except self.api.CognitiveFaceException as exception:
            logger.log(exception)
        finally:
            return candidates

    def save(self):
        """Save a new person group in MS service"""
        logger.log('Saving person group...')
        # Only create group if it does not exist
        if self.isExisted() is False:
            try:
                self.api.person_group.create(self.group.id, self.group.name)
                logger.log(
                    'Created person group with name %s' % self.group.name
                )
                return True
            except self.api.CognitiveFaceException as exception:
                logger.log(exception)
                return False
        return True

    def isExisted(self):
        """Check if group is existed or not"""
        try:
            self.api.person_group.get(self.group.id)
            return True
        except self.api.CognitiveFaceException as exception:
            logger.log(exception)
            return False

    def train(self):
        """Enqueue a group to be trained"""
        logger.log('Enqueue group training task...')
        result = self.api.person_group.train(self.group.id)
        self.processResponse(result, self.print_response)

    def trainingStatus(self):
        """Get training status"""
        logger.log('Fetching training status...')
        result = self.api.person_group.get_status(self.group.id)
        return self.processResponse(result, self.print_response)

    def processResponse(self, response, callback=None):
        response = self.dictionarize(response)
        if callback:
            callback(response)
        return response
