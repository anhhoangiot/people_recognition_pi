#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

'''
Copyright (c) 2016 Anh Hoang

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

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

            