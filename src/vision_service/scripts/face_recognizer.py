#!/usr/bin/env python

from vision_service.srv import *
import rospy
import os
from time import sleep

PATH = '/home/roboy/vision_workspace/Vision/PYTHON3_COMM/'

def check_file(object_id):
    name = ''
    os.mknod(PATH + 'request')
    while(not os.path.exists(PATH + 'out')):
        sleep(0.1)
	continue
    file = open(PATH + 'out', 'r') 
    name = file.read()
    os.remove(PATH + 'out') 
    return name

def recognize_face_server():
    rospy.init_node('recognize_face_service')
    s = rospy.Service('recognize_face', recognition, check_file)
    print "Service ready."
    rospy.spin()

if __name__ == "__main__":
    if os.path.exists(PATH + 'out'):
	os.remove(PATH + 'out')
    if os.path.exists(PATH + 'request'):
	os.remove(PATH + 'request')
    recognize_face_server()
