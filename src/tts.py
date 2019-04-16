#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, "/home/mh/.venv/SkRbts2019/lib/python2.7/site-packages/")

import requests
import settings

import rospy
from std_msgs.msg import String, Empty

def tts(msg):
    #os.system('echo "{}" | festival --tts --language russian'.format(msg.data))
    r = requests.get('http://{}/tts'.format(settings.ASR_ENDPOINT),
                 params={'query': msg.data, 'voice': 'Borisenko'})

    with open('./tts.wav', 'wb') as outfile:
        outfile.write(r.content)
    os.system('aplay ./tts.wav')
    ww_pub.publish()


if __name__ == "__main__":
    rospy.init_node('tts')
    rospy.Subscriber("/tts/text", String, tts)
    rospy.Subscriber("/nlp/text", String, tts)
    ww_pub = rospy.Publisher('/ww/trig/', Empty, queue_size=1)

    rospy.spin()