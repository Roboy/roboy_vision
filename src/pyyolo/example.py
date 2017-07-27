import pyyolo
import numpy as np
import sys
import cv2
import imutils

darknet_path = './darknet'
datacfg = 'cfg/coco.data'
cfgfile = 'cfg/tiny-yolo.cfg'
weightfile = '../tiny-yolo.weights'
#filename = darknet_path + '/data/person.jpg'
filename = "/home/roboy/outputRoboy.mp4"
thresh = 0.24
hier_thresh = 0.5
cam = cv2.VideoCapture(filename)
ret_val, img = cam.read()
print(ret_val)
if not ret_val:
	sys.exit()
pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outVideo = cv2.VideoWriter('outputRoboySkyfall.mp4',fourcc, 20.0, (800,533))
 
print('----- test python API using a file')
while True:
	ok,img = cam.read()
	frame = imutils.resize(img, width=800)
	if not img.any():
		sys.exit()
	img = img.transpose(2,0,1)
	c, h, w = img.shape[0], img.shape[1], img.shape[2]
	print w, h, c 
	data = img.ravel()/255.0
	data = np.ascontiguousarray(data, dtype=np.float32)
	outputs = pyyolo.detect(w, h, c, data, thresh, hier_thresh)	
	for output in outputs:
		print(output)
		p1 = (output['left'],output['top'])
		p2 = (output['right'],output['bottom'])
		print(p1,p2)
		cv2.rectangle(frame,p1,p2,(0,0,255,10))
		outVideo.write(frame)
# free model
pyyolo.cleanup()
