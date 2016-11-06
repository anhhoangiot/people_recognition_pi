#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-08
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0

from commons import Configurator
from controllers import CameraController
from commons import EventLogger
import threading
import time
import argparse


def setup(condition):
    Configurator.config_application()
    with condition:
        condition.notifyAll()


def start(condition, data_path=None, interval=0, register_new=True):
    with condition:
        camera = CameraController()
        if data_path:
            condition.wait()
            camera.register(data_path)
        if interval > 0:
            while True:
                camera.identify(register_new)
                time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_path')
    parser.add_argument('-i', '--interval', type=float)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-r', '--register_new', action='store_true')

    args = parser.parse_args()
    condition = threading.Condition()

    EventLogger.logger(verbose=args.verbose)

    if args.data_path:
        setUpThread = threading.Thread(
            name="setup",
            target=setup,
            args=(condition,)
        )
        mainThread = threading.Thread(
            name="main",
            target=start,
            args=(condition, args.data_path, 0, args.register_new)
        )
        setUpThread.start()
        mainThread.start()

    if args.interval:
        mainThread = threading.Thread(
            name="main",
            target=start,
            args=(condition, None, args.interval,)
        )
        mainThread.start()
