#!/usr/bin/env python

from vision_service.srv import *
import rospy
import os

PATH = '/home/roboy/vision_ws/PYTHON3_COMM/face'

def check_file(arg):
    return os.path.exists(PATH)

def recognize_face_server():
    rospy.init_node('detect_face_service')
    s = rospy.Service('detect_face', wakeup, check_file)
    print "Service ready."
    rospy.spin()

if __name__ == "__main__":
    if os.path.exists(PATH):
	os.remove(PATH)
    recognize_face_server()
