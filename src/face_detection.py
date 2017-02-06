#Debugging
import pdb
#pdb.set_trace()

# ROS imports
import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *
from vision.msg import *


## Logging
import logging
logging.basicConfig(level = logging.INFO)

#mxnet
import mxnet as mx
from mtcnn_detector import MtcnnDetector

#basic imports
import cv2
import time
import os
import numpy as np

## Realsense libraries
import pyrealsense as pyrs
from PIL import Image


if __name__ == '__main__':

    	## start pyrealsense service
	pyrs.start()

	#Image Size (define size of image)
	x_pixel = 640
	y_pixel = 480

	# resize for faster processing
	resize_factor = 0.5

	#init realsense device
	dev = pyrs.Device(device_id = 0, streams = [pyrs.ColourStream(width = x_pixel, height = y_pixel, fps = 30), pyrs.DepthStream()])
	
	#ROS INIT
	vision_object_pub = rospy.Publisher('vision_objects', VisionObject, queue_size=10)
	keypoints_pub = rospy.Publisher('object_keypoints', ObjectKeypoints, queue_size=10)
	pose_pub = rospy.Publisher('object_pose', ObjectPose, queue_size=10)
        rospy.init_node('face_detection', anonymous=True)

	# Face Detection NN
	detector = MtcnnDetector(model_folder='model', ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)


	while True:  
	    
	    # Get Frame from Realsense
	    dev.wait_for_frame()
	    c = dev.colour	    
	    c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
	    d = dev.depth*  dev.depth_scale * 1000
	    #print(c.shape)

    	    #resize images
	    img = cv2.resize(c, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
	    d_img = cv2.resize(d, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
	    d_img = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_RAINBOW)

	    # Detect and align faces using MTCNN
	    results = detector.detect_face(img)
	    if results is None:
		#only print img if no face found
	  	cv2.imshow("detection result", c)
		cv2.waitKey(10)
	        continue
	    total_boxes = results[0]
	    points = results[1]
	

 	    #Show detection result
	    draw = c.copy()
	    #loop detected faces (boxes)
	    for b in total_boxes:
		cv2.rectangle(draw, (int(b[0]/resize_factor), int(b[1]/resize_factor)), (int(b[2]/resize_factor), int(b[3]/resize_factor)), (255, 255, 255))
	    #Loop face alignment (points)
	    for p in points:
		for i in range(5):
		    cv2.circle(draw, (int(p[i]/resize_factor), int(p[i + 5]/resize_factor)), 1, (0, 0, 255), 3)
	    # Show Picture
	    cv2.imshow("detection result", draw)	
  
	    #publish ROS Topics
	    object_id = 0
	    #Loop face alignment (points)
	    for p in points:
		#points in p: 1 left eye, 2 right eye, 3 nose, 4 left mouth point, 5 right mouth point

		#TODO: get depth at point 3 for distance and recalculate position in metres
		# position(x,y,z)
		position = Point(p[3],p[8],d[int(p[3]),int(p[8])])

		#TODO calculate Orientation from reference points
		orientation = Quaternion()

		key_points = []
		for x in range(5):
		    key_points.append(Point(p[i],p[i+5],0))
		object_pose = Pose(position,orientation)
		
	       #Fill ROS msg
		header = Header(0,rospy.Time.now(),str(0))
		object_type = "face"
		vision_object = VisionObject()
		vision_object.header = header
		vision_object.object_id = object_id
		vision_object.object_pose = object_pose
		vision_object.object_type = object_type
		vision_object.key_points = key_points
		object_pose = ObjectPose(header, object_id, object_type, object_pose)
		object_keypoints = ObjectKeypoints(header, object_id, object_type, key_points)

		#publish
	        vision_object_pub.publish(vision_object)
		pose_pub.publish(object_pose)
		keypoints_pub.publish(object_keypoints)
  	        object_id += 1

	    #WAIT
	    cv2.waitKey(10)

