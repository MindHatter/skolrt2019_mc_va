#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, "/home/mh/.venv/SkRbts2019/lib/python2.7/site-packages/")


import random
import requests
from recorder import Record

import rospy
from std_msgs.msg import String, Empty

import settings


class STT():
    def __init__(self, engine):
        if engine == "wit":
            self.recognize = self._wit

    def _wit(self, audio):
        headers = {'authorization': 'Bearer ' + settings.WIT_ACCESS_TOKEN,
                'Content-Type': 'audio/wav'}

        try:
            resp = dict(requests.post('https://api.wit.ai/speech', 
                headers = headers,
                data = audio).json())
            data = resp[u'_text']
            
        except Exception as e:
            print(e)
            data = ''
        return data

    def _unknown(self):
        answers = [
            'Моя тебя не понимать',
            'Мы точно на одной волне? повторите, пожалуйста',
            'Не понятно. скажите еще разок',
            'И что это вы сейчас такое сказали?',
        ]
        return random.choice(answers)

def stt_call(msg):
    recorder.record_to_file()
    audio = recorder.read_from_file()
    data = stt.recognize(audio)
    print(data)
    if data:
        stt_pub.publish(data)
    else:
        tts_pub.publish(stt._unknown())
        ww_pub.publish()

if __name__ == '__main__':
    recorder = Record()
    stt = STT(settings.STT_ENGINE)

    rospy.init_node('stt')
    stt_pub = rospy.Publisher('/stt/text', String, queue_size=1)
    tts_pub = rospy.Publisher('/tts/text', String, queue_size=1)
    ww_pub = rospy.Publisher('/ww/trig/', Empty, queue_size=1)
    ww_sub = rospy.Subscriber('/ww/detected/', Empty, stt_call)
    rospy.spin()