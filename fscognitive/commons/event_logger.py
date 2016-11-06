#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

import thread
import time


class EventLogger(object):
    """Logger for all events"""
    instance = None

    @classmethod
    def logger(cls, verbose=True):
        if cls.instance is None:
            cls.instance = cls(verbose)
        return cls.instance

    def __init__(self, verbose):
        super(EventLogger, self).__init__()
        self.logs_queue = []
        self.verbose = verbose
        print verbose
        self.log_events()

    def log(self, log):
        self.logs_queue.append(log)

    def log_events(self):
        if self.verbose is True:
            thread.start_new_thread(self.__log, ())

    def __log(self):
        while True:
            if self.logs_queue is not None:
                if len(self.logs_queue) > 0:
                    log = self.logs_queue.pop(0)
                    print log
            else:
                time.sleep(1)
