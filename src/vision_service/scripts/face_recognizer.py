## @package face_recognizer
#  This module provides a service to trigger the classification of a detected face and returns the face name.
#  
#  This module should be integrated with face recognition module as soon as it exists. As a current workaround this module
#  communciates with face_detection module using file I/O.
#  The reason for this workaround is a missing Python 3 support for ROS. Since Face_detection and recognition runs using python 3
#  this service using ROS can be run seperatly using python 2.7.
#  Calling the service: rosservice call /recognize_face 'face_id'

from vision_service.srv import *
import rospy
import os
from time import sleep

# Path to be used for file I/O communication (env variable)
PATH = os.environ['VISION_COMM_PATH']


## Helper function for file I/O communciation
#
#  @param object_id The id of the face to be recognized
#  @return The name of the recognized face
def check_file(object_id):
    name = ''

    # make request file
    os.mknod(PATH + 'request')
    i = 0

    # check if request file is deleted by face_detection module within 0.2 seconds.
    # Timeout otherwise.
    while (True):
        sleep(0.02)
        if not os.path.exists(PATH + 'request'):
            break
        if (i > 10):
            if os.path.exists(PATH + 'request'):
                os.remove(PATH + 'request')
                print('Timeout')
            return ''
        i += 1

    # Wait for result file to be written
    while (not os.path.exists(PATH + 'out')):
        sleep(0.1)

    # read result
    file = open(PATH + 'out', 'r')
    name = file.read()

    # remove result file
    os.remove(PATH + 'out')
    return name


## Function to start the ROS Service for face recognition
def recognize_face_server():
    rospy.init_node('recognize_face_service')
    s = rospy.Service('recognize_face', recognition, check_file)
    print "Face recognition service ready. Call with name 'recognize_face'."
    rospy.spin()


## Main Method
if __name__ == "__main__":
    if os.path.exists(PATH + 'out'):
        os.remove(PATH + 'out')
    if os.path.exists(PATH + 'request'):
        os.remove(PATH + 'request')
    recognize_face_server()
