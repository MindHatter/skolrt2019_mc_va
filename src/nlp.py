#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, "/home/mh/.venv/SkRbts2019/lib/python2.7/site-packages/")

import requests
import settings

import rospy
from std_msgs.msg import String

def nlp(msg):
    r = requests.get("http://{}/text_request".format(settings.ASR_ENDPOINT),
        params={
            'voice': 'Borisenko',
            'chitchat': 1,
            'query': msg.data,
            'need_audio_response': 0})

    resp = r.json()
    print(resp['response_text'])
    nlp_pub.publish(resp['response_text'])
    

if __name__ == "__main__":
    rospy.init_node('nlp')

    rospy.Subscriber("/stt/text", String, nlp)
    nlp_pub = rospy.Publisher("/nlp/text", String, queue_size=1)
    rospy.spin()