## @package face_detector
#  This module provides a service to check for faces nearby. The actual calculation is done in face_detection module.
#  
#  This module should be integrated with face detection module. As a current workaround this module
#  communciates with face_detection module using file I/O.
#  The reason for this workaround is a missing Python 3 support for ROS. Since Face_detection and recognition runs using python 3
#  this service using ROS can be run seperatly using python 2.7.
#  Calling the service: rosservice call /detect_face

from vision_service.srv import *
import rospy
import os

# Path to be used for file I/O communication (env variable)
PATH = os.environ['VISION_COMM_PATH']


## Helper function for file I/O communciation
#
#  @return True if a face was detected nearby
def check_file(arg):
    return os.path.exists(PATH + 'face')


## Function to start the ROS Service for face detection
def recognize_face_server():
    rospy.init_node('detect_face_service')
    s = rospy.Service('detect_face', wakeup, check_file)
    print "Face Detection Service ready. Call with name '/detect_face'."
    rospy.spin()


## Main Method
if __name__ == "__main__":
    if os.path.exists(PATH + 'face'):
        os.remove(PATH + 'face')
    recognize_face_server()
