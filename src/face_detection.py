
#Dirty Hacks to run on Roboy Nuke
# Before running also activate the conda environment: source /home/roboy/anaconda3/bin/activate roboy
import sys 
sys.path = ['/home/roboy/anaconda3/envs/roboy/lib/python3.6/site-packages'] + sys.path
sys.path.append('/home/roboy/vision_workspace/Vision/')

#basic imports
import numpy as np
import cv2
import os
from scipy import misc
import time

#Import for NNs
import tensorflow as tf
from models.mtcnn import detect_face

#Threads
from thread import start_new_thread

## Realsense libraries
import pyrealsense as pyrs

# Define of standard face size for alignment
EXPECT_SIZE = 160
#Define of path for Communication to ROS using I/O on file system
COMM_PATH = '/home/roboy/vision_workspace/Vision/PYTHON3_COMM/'

# Detect faces and landmarks using MTCNN Network
def detect_face_and_landmarks_mtcnn(img):
    img = img[:,:,0:3]
    bbs, lms = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    boxes = []
    landmarks = []
    face_index = 0
    for r in bbs:
        r = r.astype(int)
        points = []
        for i in range(5):
            points.append((lms[i][face_index] , lms[i+5][face_index]))
        landmarks.append(points)
        boxes.append((r[0] , r[1] , r[2] , r[3]))
        #boxes.append(r[:4].astype(int).tolist())
        face_index += 1
    return boxes, landmarks

# Align Found Faces found by MTCNN Network (= crop face region)
def align_face_mtcnn(img, bb, landmarks):
    assert isinstance(bb, tuple)
    cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
    scaled = misc.imresize(cropped, (EXPECT_SIZE, EXPECT_SIZE), interp='bilinear')
    return scaled	

# Function to draw found bounding boxes
def draw_rects(image, rects, resize_factor):
    result = image.copy()
    rects = (np.array(rects)/resize_factor).astype(int)
    for left, top, right, bottom in rects:
        cv2.rectangle(result, (left, top), (right, bottom), (0, 255, 0), 2)
    return result

#Function to draw found landmarks
def draw_landmarks(image, points, resize_factor):
    result = image.copy()
    for face_points in points:
    	#face_points = np.array(face_points)/resize_factor
    	#print(face_points)
    	#face_points = (np.array(face_points)/resize_factor).astype(int)
    	for point in face_points:
    		point = (int(point[0]/resize_factor), int(point[1]/resize_factor))
    		cv2.circle(result, point, 3, (0, 255, 0), -1 )
    return result	
	
# Function to check if a face appears in certain size
FACE_AREA = 1500 # Face area for approx. 1.5m distance
def face_detected(bounding_boxes):
	face_area = 0
	for left, top, right, bottom in bounding_boxes:
		tmp_face_area = (right-left) * (bottom-top)
		if(tmp_face_area > face_area):
			face_area = tmp_face_area
	if(face_area > FACE_AREA):
		return True
	else:
		return False

# Function to recognize a face using facenet
def recognize_face(face_img):
	#TODO: Implementation of Facenet + classification
	time.sleep(1)
	face_name = "TEST"

	# write back result
	f = open(COMM_PATH + 'out', 'w')
	f.write(face_name)
	f.close()
	
	# delete running flag
	os.remove(COMM_PATH + 'running')

	print('done!')
	return

# MAIN
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

	# Face Detection NN
	sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
	pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
	minsize = 20 # minimum size of face
	threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
	factor = 0.709 # scale factor

	# store how many following frames no Face was detected.
	no_face_detect_counter = 0

	while True:  
	    # Get Frame from Realsense
		dev.wait_for_frame()
		# color image	    
		c = cv2.cvtColor(dev.colour, cv2.COLOR_RGB2BGR)
		#depth images
		d = dev.depth*  dev.depth_scale * 1000

    	#resize images for faster processing with resize_factor
		img = cv2.resize(c, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
		
		d_img = cv2.resize(d, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
		d_img = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_RAINBOW)
		
		# Detect and align faces using MTCNN
		total_boxes, points = detect_face_and_landmarks_mtcnn(img)
		
		#only print img if no face found
		if len(total_boxes) is 0:
			# remove face nearby flag (File I/O)
			no_face_detect_counter+=1
			if no_face_detect_counter > 3:
			    if os.path.exists(COMM_PATH + 'face'):
				    os.remove(COMM_PATH + 'face')
			# show image and continue
			cv2.imshow("detection result", c)
			cv2.waitKey(10)
			continue

		# Check if faces nearby and communicate to ROS using file I/O
		if face_detected(total_boxes):
			if not os.path.exists(COMM_PATH + 'face'):
				no_face_detect_counter = 0
				os.mknod(COMM_PATH + 'face')
		else:
			no_face_detect_counter+=1
			if no_face_detect_counter > 3:
				if os.path.exists(COMM_PATH + 'face'):
					os.remove(COMM_PATH + 'face')

		## Call Face Recognition if Service has been triggered
		if os.path.exists(COMM_PATH + 'request'):
			if not os.path.exists(COMM_PATH + 'running'):
				# create running flag
				os.mknod(COMM_PATH + 'running')
				# delete request flag
				os.remove(COMM_PATH + 'request')
				# start recognition thread
				start_new_thread(recognize_face,(total_boxes[0],))

		
		#Show detection result
		draw = c.copy()
		draw = draw_rects(draw, total_boxes, resize_factor)
		draw = draw_landmarks(draw, points, resize_factor)

		cv2.imshow("detection result", draw)	

	    #WAIT
		cv2.waitKey(10)

