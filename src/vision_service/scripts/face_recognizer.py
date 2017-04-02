#!/usr/bin/env python

from vision_service.srv import *
import rospy
import os
from time import sleep

PATH = '/home/roboy/vision_workspace/Vision/PYTHON3_COMM/'

def check_file(object_id):
    name = ''
    os.mknod(PATH + 'request')
    while(os.path.exists(PATH + 'request')):
        sleep(0.1)
	continue
    if os.path.exists(PATH + 'face'):
	file = open(PATH + 'face', 'r') 
	name = file.read() 
    return name

def recognize_face_server():
    rospy.init_node('recognize_face_service')
    s = rospy.Service('recognize_face', recognition, check_file)
    print "Service ready."
    rospy.spin()

if __name__ == "__main__":
    if os.path.exists(PATH + 'face'):
	os.remove(PATH + 'face')
    if os.path.exists(PATH + 'request'):
	os.remove(PATH + 'request')
    recognize_face_server()
