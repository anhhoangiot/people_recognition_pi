#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

import os


class Utilities:
    @staticmethod
    def file_exists(filePath):
        dir = os.path.dirname(__file__)
        absolutePath = os.path.join(dir, filePath)
        if os.path.exists(absolutePath) is False:
            print 'File not exist at path %s' % filePath
        return os.path.exists(absolutePath)

    @staticmethod
    def delete_file(filePath):
        dir = os.path.dirname(__file__)
        absolutePath = os.path.join(dir, filePath)
        if os.path.exists(absolutePath) is True:
            os.remove(absolutePath)
            print 'Deleted file at path %s' % filePath
        return os.path.exists(absolutePath)

    @staticmethod
    def absolute_path(directory, fileName):
        if os.path.isdir(directory):
            return os.path.join(directory, fileName)
        else:
            dir = os.path.dirname(directory)
            return os.path.join(dir, fileName)

    @staticmethod
    def project_directory():
        return os.path.dirname(__file__).strip('commons/')

    @staticmethod
    def train_data_path():
        return os.path.join(
            Utilities.project_directory(),
            'resources\\datasets\\')

    @staticmethod
    def alias_path(alias):
        return os.path.join(Utilities.train_data_path(), alias)

    @staticmethod
    def voices_path():
        return os.path.join(
            Utilities.project_directory(),
            'resources\\sounds\\names\\')
