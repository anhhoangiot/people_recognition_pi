#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-10
# @Author  : Anh Hoang (anhhoang.work.mail@gmail.com)
# @Project : FSCognitive
# @Version : 1.0


import requests
import wget
import pygame
import os
import time
from commons import Utilities


class Speaker():
    def __init__(self):
        super(Speaker, self).__init__()

    @staticmethod
    def speak(alias):
        sounds_dir = Utilities.voices_path()
        save_dir = Utilities.absolute_path(sounds_dir, alias + '.mp3')
        if os.path.exists(save_dir) is True:
            # print save_dir
            pygame.mixer.init(44100, -16, 2, 2048)
            pygame.mixer.music.load(save_dir)
            pygame.mixer.music.play()
            time.sleep(1.05)

    @staticmethod
    def create_voice(text, alias):
        sounds_dir = Utilities.voices_path()
        save_dir = Utilities.absolute_path(sounds_dir, alias + '.mp3')
        if os.path.exists(save_dir) is False:
            headers = {
                'Content-Type': 'application/json',
                'api_key': 'b5db987b5a944ff78097d435a5a564dc'
            }
            try:
                response = requests.request(
                    'POST',
                    'http://api.openfpt.vn/text2speech/v3',
                    headers=headers,
                    data=text
                )
                if response.status_code not in (200, 202):
                    print response.status_code
                if response.text:
                    result = response.json()
                    if result['async']:
                        wget.download(result['async'], save_dir)
            except Exception as e:
                print e
