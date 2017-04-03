#!/usr/bin/env python

from vision_service.srv import *
import rospy
import os

PATH = os.environ['VISION_COMM_PATH']

def check_file(arg):
    return os.path.exists(PATH + 'face')

def recognize_face_server():
    rospy.init_node('detect_face_service')
    s = rospy.Service('detect_face', wakeup, check_file)
    print "Face Detection Service ready. Call with name '/detect_face'."
    rospy.spin()

if __name__ == "__main__":
    if os.path.exists(PATH + 'face'):
		os.remove(PATH + 'face')
    recognize_face_server()
