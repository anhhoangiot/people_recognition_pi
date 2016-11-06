#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from multiprocessing import Process


class ProcessParallel(object):
    """
    To Process the  functions parallely

    """
    def __init__(self, *jobs):
        """
        """
        self.jobs = jobs
        self.processes = []

    def fork_processes(self):
        """
        Creates the process objects for given function deligates
        """
        for job in self.jobs:
            proc = Process(target=job)
            self.processes.append(proc)

    def fork_threads(self):
        for job in self.jobs:
            self.processes.append(job)

    def start_all(self):
        """
        Starts the functions process all together.
        """
        for proc in self.processes:
            proc.start()

    def join_all(self):
        """
        Waits untill all the functions executed.
        """
        for proc in self.processes:
            proc.join()
