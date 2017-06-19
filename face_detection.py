import sys 
import numpy as np
import cv2
import os
from scipy import misc
import time
import re
import pickle

#Import for NNs
import tensorflow as tf
from models.mtcnn import detect_face

#Threads


## Realsense libraries
#import pyrealsense as pyrs

# Define of standard face size for alignment
EXPECT_SIZE = 160
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
		face_index += 1
	return boxes, landmarks

# Align Found Faces found by MTCNN Network (= crop face region)
# def align_face_mtcnn(img, bb):
# 	assert isinstance(bb, tuple)
# 	cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
# 	scaled = misc.imresize(cropped, (EXPECT_SIZE, EXPECT_SIZE), interp='bilinear')
# 	return scaled	

# Function to draw found bounding boxes
def draw_rects(image, rects, resize_factor):
	result = image.copy()
	rects = (np.array(rects)/resize_factor).astype(int)
	print (rects);
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

# get the id of the bounding box of the closest face
def get_closest_face(bounding_boxes):
	i = 0
	max_id = 0
	face_area = 0
	for left, top, right, bottom in bounding_boxes:
		tmp_face_area = (right-left) * (bottom-top)
		if(tmp_face_area > face_area):
			max_id = i
			face_area = tmp_face_area
		i+=1
	return max_id

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

# function for importing facenet
def load_model(model_dir, model_meta, model_content):
	s = tf.InteractiveSession()
	model_dir_exp = os.path.expanduser(model_dir)
	saver = tf.train.import_meta_graph(os.path.join(model_dir_exp, meta_file))
	saver.restore(tf.get_default_session(), os.path.join(model_dir_exp, ckpt_file))
	tf.get_default_graph().as_graph_def()
	return s

# helper function for importing facenet
def get_model_filenames(model_dir):
	files = os.listdir(model_dir)
	meta_files = [s for s in files if s.endswith('.meta')]
	if len(meta_files)==0:
		raise ValueError('No meta file found in the model directory (%s)' % model_dir)
	elif len(meta_files)>1:
		raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
	meta_file = meta_files[0]
	meta_files = [s for s in files if '.ckpt' in s]
	max_step = -1
	for f in files:
		step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
		if step_str is not None and len(step_str.groups())>=2:
			step = int(step_str.groups()[1])
			if step > max_step:
				max_step = step
				ckpt_file = step_str.groups()[0]
	return meta_file, ckpt_file

# MAIN
if __name__ == '__main__':

	
	#Image Size (define size of image)
	x_pixel = 640
	y_pixel = 480

	# resize for faster processing
	#resize_factor = 0.5
	resize_factor = 1
	# store whether a face was detected nearby
	face_nearby = False
	
	# store how many following frames no Face was detected nearby
	no_face_detect_counter = 0

	# Face Detection NN
	sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
	pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
	minsize = 20 # minimum size of face
	threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
	factor = 0.709 # scale factor

	#tracker = cv2.Tracker_create("MIL")
	tracker = cv2.MultiTracker("MIL")
	video = cv2.VideoCapture("/Users/prashanth/code/roboy/Vision/videos/trackingRajini.mp4")
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	outVideo = cv2.VideoWriter('outputRajini.mp4',fourcc, 20.0, (640,480))
	if not video.isOpened():
		print ("Could not open video");
		sys.exit();
 
	# Read first frame.
	ok, frame = video.read()
	if not ok:
		print ('Cannot read video file')
		sys.exit()
	print('Starting detection...')
	frame_count = 0;
	bbox=();
	while frame_count < 5:  	
		frame_count+=1;    
		ok, frame = video.read()
		if not ok:
			print ('Cannot read video file')
			sys.exit()
		print('Starting detection...')

		c = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		
		#resize images for faster processing with resize_factor
		img = cv2.resize(c, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
		
		
		# Detect and align faces using MTCNN
		total_boxes, points = detect_face_and_landmarks_mtcnn(img)
		
		#only print img if no face found
		if len(total_boxes) is 0:
			# remove face nearby flag (File I/O)
			no_face_detect_counter+=1
			if no_face_detect_counter > 3:
				face_nearby = False
			# show image and continue
			cv2.imshow("detection result", c)
			cv2.waitKey(10)
			continue

		
		
		# #Show detection result
		#print (points);
		draw = draw_rects(img.copy(), total_boxes, resize_factor)
		draw = draw_landmarks(draw, points, resize_factor)

		cv2.imshow("detection result", draw)	
		bbox = (np.array(total_boxes)/resize_factor).astype(int);
		#print (bbox);
		#WAIT
		cv2.waitKey(10)
	ok, frame = video.read()
	trackPoints = (bbox[0][0],bbox[0][1],bbox[0][2]-bbox[0][0],bbox[0][3]-bbox[0][1]);
	trackPoints2 = (bbox[1][0],bbox[1][1],bbox[1][2]-bbox[1][0],bbox[1][3]-bbox[1][1]);
	image = cv2.resize(frame, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
	print (trackPoints);
	print (trackPoints2);
	#ok = tracker.init(image, trackPoints)
	ok = tracker.add(image, trackPoints);
	ok = tracker.add(image, trackPoints2);
	while True:
		# Read a new frame
		#print("Starting to track now");
		ok, frame = video.read()
		if not ok:
			break
		 
		# Update tracker
		img = cv2.resize(frame, (int(resize_factor*x_pixel),int(resize_factor*y_pixel)))
		# ok, trackPoints = tracker.update(img)
		# #print (bbox);
		# # Draw bounding box
		# if ok:
		# 	p1 = (int(trackPoints[0]), int(trackPoints[1]))
		# 	#p2 = (int(bbox[0][2]) , int (bbox[0][3]))
		# 	p2 = (int(trackPoints[0] + trackPoints[2]), int(trackPoints[1] + trackPoints[3]));
		# 	cv2.rectangle(img, p1, p2, (0,0,255))
 
		ok, boxes = tracker.update(img)
		print (ok,boxes)

		for newbox in boxes:
			p1 = (int(newbox[0]), int(newbox[1]))
			p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
			cv2.rectangle(img, p1, p2, (0,0,255,10))

		outVideo.write(img)
		# Display result
		cv2.imshow("detection result", img)
		# Exit if ESC pressed
		cv2.waitKey(10) 
		
