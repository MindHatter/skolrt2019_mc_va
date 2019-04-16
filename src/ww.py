#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, "/home/mh/.venv/SkRbts2019/lib/python2.7/site-packages/")
sys.path.insert(0, "/home/mh/ros_ws/src/va/snowboy/examples/Python")

import snowboydecoder
import signal


import rospy
from std_msgs.msg import Empty

interrupted = False

detected = True

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def ww_cb(msg):
    global detected
    detected = True

def detected_cb():
    global detected
    if detected:
        print("detected")
        os.system("aplay /home/mh/ros_ws/src/va/sfx/beep.wav")
        ww_pub.publish()
    detected = False

if __name__ == "__main__":
    
    rospy.init_node("ww")
    rospy.Subscriber("ww/trig", Empty, ww_cb)
    ww_pub = rospy.Publisher("ww/detected", Empty, queue_size=1)

    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector("/home/mh/ros_ws/src/va/src/skolkovo.pmdl", sensitivity=0.5, audio_gain=1)
    detector.start(detected_cb, interrupt_check=interrupt_callback)
    detector.terminate()