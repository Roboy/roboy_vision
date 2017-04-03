
#Dirty Hacks to run on Roboy Nuke
# Before running also activate the conda environment: 

#basic imports#
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
from thread import start_new_thread

## Realsense libraries
import pyrealsense as pyrs

# Define of standard face size for alignment
EXPECT_SIZE = 160

#------- Communication workaround -----------
#Define of path for Communication to ROS using I/O on file system
COMM_PATH = os.environ['VISION_COMM_PATH']
#--------------------------------------------

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
def align_face_mtcnn(img, bb):
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
def recognize_face(face_img, session, classifier):

	feed_dict = {image_batch: np.expand_dims(face_img , 0), phase_train_placeholder: False }
	rep = session.run(embeddings, feed_dict=feed_dict)[0]
	out = clf.predict(rep.reshape(1,-1))
	names = np.load('models/lfw_embeddings/facenet_names.npy')
	face_name = names[out[0]]
	
	#------- Communication workaround -----------
	# write back result
	f = open(COMM_PATH + 'out', 'w')
	f.write(face_name)
	f.close()
	# delete running flag
	os.remove(COMM_PATH + 'running')
	#--------------------------------------------
	
	print('classification successful!')
	return face_name

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

	#------- Communication workaround -----------
	# remove all COMM Files
	if os.path.exists(COMM_PATH + 'request'):
		os.remove(COMM_PATH + 'request')
	if os.path.exists(COMM_PATH + 'face'):
		os.remove(COMM_PATH + 'face')
	if os.path.exists(COMM_PATH + 'out'):
		os.remove(COMM_PATH + 'out')
	if os.path.exists(COMM_PATH + 'running'):
		os.remove(COMM_PATH + 'running')
	#--------------------------------------------
	
    ## start pyrealsense service
	pyrs.start()

	#Image Size (define size of image)
	x_pixel = 640
	y_pixel = 480

	# resize for faster processing
	resize_factor = 0.5
	
	# store whether a face was detected nearby
	face_nearby = False
	
	# store how many following frames no Face was detected nearby
	no_face_detect_counter = 0
	
	#init realsense device
	dev = pyrs.Device(device_id = 0, streams = [pyrs.ColourStream(width = x_pixel, height = y_pixel, fps = 30), pyrs.DepthStream()])

	# Face Detection NN
	sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
	pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
	minsize = 20 # minimum size of face
	threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
	factor = 0.709 # scale factor


	# Face Recognition Facenet NN
	print('Loading Facenet...')
	svm_model = "models/SVM/svm_lfw.mod"
	clf = pickle.load( open( svm_model, "rb" ) )
	model_dir = 'models/facenet'
	meta_file, ckpt_file = get_model_filenames(os.path.expanduser(model_dir))
	session = load_model(model_dir, meta_file, ckpt_file)
	graph = tf.get_default_graph()
	image_batch = graph.get_tensor_by_name("input:0")
	phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")
	embeddings = graph.get_tensor_by_name("embeddings:0")
	print('done.')
	

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
				face_nearby = False
				#------- Communication workaround -----------
				if os.path.exists(COMM_PATH + 'face'):
					os.remove(COMM_PATH + 'face')
				#--------------------------------------------
			# show image and continue
			cv2.imshow("detection result", c)
			cv2.waitKey(10)
			continue

		
		# Check if faces nearby and communicate to ROS using file I/O
		if face_detected(total_boxes):
			face_nearby = True
			#------- Communication workaround -----------
			if not os.path.exists(COMM_PATH + 'face'):
				no_face_detect_counter = 0
				os.mknod(COMM_PATH + 'face')
			#--------------------------------------------
		else:
			no_face_detect_counter+=1
			if no_face_detect_counter > 3:
				face_nearby = False
				#------- Communication workaround -----------
				if os.path.exists(COMM_PATH + 'face'):
					os.remove(COMM_PATH + 'face')
				#--------------------------------------------
		
		#------- Communication workaround -----------
		## Call Face Recognition if Service has been triggered
		if os.path.exists(COMM_PATH + 'request'):
			if not os.path.exists(COMM_PATH + 'running'):
				# create running flag
				os.mknod(COMM_PATH + 'running')
				# delete request flag
				os.remove(COMM_PATH + 'request')
				# start recognition thread
				start_new_thread(recognize_face,(align_face_mtcnn(img,total_boxes[0]), session, clf,))
		#--------------------------------------------
		
		## TODO:
		# - remove all communication workaround blocks
		# - create ros service returning face_nearby
		# - create ros service calling recognize_face(face_img, session, classifier) and returning classification result
		
		#Show detection result
		draw = draw_rects(c.copy(), total_boxes, resize_factor)
		draw = draw_landmarks(draw, points, resize_factor)

		cv2.imshow("detection result", draw)	

	    #WAIT
		cv2.waitKey(10)

